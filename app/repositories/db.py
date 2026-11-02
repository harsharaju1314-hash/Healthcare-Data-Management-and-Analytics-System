"""
Database Connection and Session Management
Supports Oracle Database Free (23c/21c via python-oracledb) with seamless SQLite
fallback for unit testing and local development environments without an active Oracle instance.
"""

import os
import sqlite3
from contextlib import contextmanager
from decimal import Decimal
from datetime import datetime, date
from typing import List, Dict, Any, Optional, Tuple

from config import get_config
from app.utils.logger import logger
from app.utils.exceptions import DatabaseException, ConflictException

# Try importing oracledb
try:
    import oracledb
    ORACLE_AVAILABLE = True
except ImportError:
    ORACLE_AVAILABLE = False


class DatabaseManager:
    """Manages database connectivity, cursor execution, and transactions."""

    def __init__(self, config=None):
        self.config = config or get_config()
        self.engine = self.config.DB_ENGINE.lower()
        self._test_connection()

    def _test_connection(self):
        """Validates database availability and sets active engine."""
        if self.engine == "oracle":
            if not ORACLE_AVAILABLE:
                logger.warning("oracledb module not available. Falling back to SQLite.")
                self.engine = "sqlite"
                return

            try:
                # Test Oracle connection with short timeout
                conn = self._get_oracle_connection()
                conn.close()
                logger.info(f"Connected successfully to Oracle Database Free ({self.config.get_oracle_dsn()})")
            except Exception as e:
                logger.warning(f"Could not connect to Oracle Database: {e}. Falling back to SQLite.")
                self.engine = "sqlite"
        else:
            logger.info(f"Using SQLite database engine at {self.config.SQLITE_DB_PATH}")

    def is_oracle(self) -> bool:
        """Returns True if current active engine is Oracle Database."""
        return self.engine == "oracle"

    def _get_oracle_connection(self):
        """Establishes an Oracle connection in thin mode."""
        return oracledb.connect(
            user=self.config.ORACLE_USER,
            password=self.config.ORACLE_PASSWORD,
            dsn=self.config.get_oracle_dsn(),
            expire_time=2,
        )

    def _get_sqlite_connection(self):
        """Establishes an SQLite connection with row factory and foreign keys enabled."""
        conn = sqlite3.connect(
            self.config.SQLITE_DB_PATH,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            timeout=15.0
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    @contextmanager
    def get_connection(self):
        """Context manager yielding an active database connection."""
        conn = None
        try:
            if self.is_oracle():
                conn = self._get_oracle_connection()
            else:
                conn = self._get_sqlite_connection()
            yield conn
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except Exception:
                    pass
            self._handle_db_exception(e)
        finally:
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass

    def _handle_db_exception(self, e: Exception):
        """Normalizes database exceptions into domain exceptions without leaking credentials."""
        err_str = str(e).lower()
        logger.error(f"Database error encountered: {e}")

        # Unique constraint violation detection
        if "unique" in err_str or "ora-00001" in err_str or "constraint failed" in err_str:
            raise ConflictException(f"Database integrity conflict: Duplicate record or constraint violation. {e}")
        # Foreign key violation
        if "foreign key" in err_str or "ora-02291" in err_str or "ora-02292" in err_str:
            raise ConflictException(f"Referential integrity violation: Referenced key does not exist or has dependents.")
        # Check constraint violation
        if "check constraint" in err_str or "ora-02290" in err_str:
            raise ConflictException(f"Data value violates database check constraint.")

        raise DatabaseException(f"Database operation failed: {e}")

    def execute_query(self, sql: str, params: Optional[Any] = None) -> List[Dict[str, Any]]:
        """Executes a query and returns a list of dictionaries with lowercase column names."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                # Oracle vs SQLite parameter binding format normalization
                formatted_sql = sql
                if self.is_oracle():
                    # Oracle uses :name or :1
                    cursor.execute(formatted_sql, params or {})
                else:
                    # SQLite supports :name or ?
                    cursor.execute(formatted_sql, params or {})

                columns = [col[0].lower() for col in cursor.description] if cursor.description else []
                rows = cursor.fetchall()
                results = []
                for row in rows:
                    row_dict = {}
                    for idx, col in enumerate(columns):
                        val = row[idx]
                        if isinstance(val, (datetime, date)):
                            row_dict[col] = val.isoformat()
                        elif isinstance(val, Decimal):
                            row_dict[col] = float(val)
                        else:
                            row_dict[col] = val
                    results.append(row_dict)
                return results
            finally:
                cursor.close()

    def execute_one(self, sql: str, params: Optional[Any] = None) -> Optional[Dict[str, Any]]:
        """Executes a query and returns a single record dictionary, or None."""
        results = self.execute_query(sql, params)
        return results[0] if results else None

    def execute_non_query(self, sql: str, params: Optional[Any] = None) -> Tuple[int, Optional[int]]:
        """
        Executes an INSERT, UPDATE, or DELETE statement.
        Returns a tuple of (rowcount, last_inserted_id).
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, params or {})
                conn.commit()
                rowcount = cursor.rowcount
                last_id = getattr(cursor, "lastrowid", None)
                return rowcount, last_id
            finally:
                cursor.close()

    def execute_transaction(self, statements: List[Tuple[str, Any]]) -> bool:
        """Executes multiple SQL statements within a single atomic transaction."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                for sql, params in statements:
                    cursor.execute(sql, params or {})
                conn.commit()
                return True
            except Exception as e:
                conn.rollback()
                self._handle_db_exception(e)
            finally:
                cursor.close()


# Singleton database instance
db = DatabaseManager()

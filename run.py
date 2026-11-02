"""
Application Entry Point
Starts the HealthPulse Flask application server with optional CLI commands.
"""

import argparse
import sys
from app import create_app
from config import get_config
from app.utils.logger import logger
from scripts.init_db import init_database
from scripts.seed_db import seed_database
from scripts.export_reports_to_csv import generate_exports

app = create_app()


def main():
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(description="Healthcare Data Management and Analytics System")
    parser.add_argument("--host", default="0.0.0.0", help="Binding host address")
    parser.add_argument("--port", type=int, default=5000, help="Port to listen on")
    parser.add_argument("--init-db", action="store_true", help="Initialize schema tables and constraints")
    parser.add_argument("--seed", action="store_true", help="Seed database with synthetic records")
    parser.add_argument("--export", action="store_true", help="Export reports to CSV for Tableau")

    args = parser.parse_args()

    if args.init_db:
        init_database()
        sys.exit(0)

    if args.seed:
        seed_database()
        sys.exit(0)

    if args.export:
        generate_exports()
        sys.exit(0)

    config = get_config()
    logger.info(f"Starting HealthPulse Healthcare Server on {args.host}:{args.port} (DB: {config.DB_ENGINE})...")
    app.run(host=args.host, port=args.port, debug=config.DEBUG)


if __name__ == "__main__":
    main()

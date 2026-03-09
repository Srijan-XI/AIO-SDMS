"""
Main entry point for AIO-SDMS when run as a module.

Usage:
    python -m aio_sdms [options]
    python -m aio_sdms --gui
    python -m aio_sdms --cli battery
    python -m aio_sdms --web --port 8080
"""

import sys
from aio_sdms.cli import main

if __name__ == "__main__":
    sys.exit(main())

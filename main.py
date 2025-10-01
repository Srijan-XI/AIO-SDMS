#!/usr/bin/env python3
"""
All-in-One System Tools - Main Entry Point
A unified system diagnostic and monitoring tool suite

Author: Srijan-XI
Date: October 1, 2025
Version: 1.0
"""

import sys
import argparse
from pathlib import Path

# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

from core.common.config import Config
from core.common.logger import Logger
from interfaces.cli.cli_interface import CLIInterface
from interfaces.gui.gui_interface import GUIInterface
from interfaces.web.web_interface import WebInterface

def main():
    """Main entry point for the All-in-One System Tools"""
    
    # Initialize configuration and logging
    config = Config()
    logger = Logger()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='All-in-One System Diagnostic & Monitoring Tools',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Available Tools:
  battery     - Battery monitoring and charging analysis
  diagnostics - Hardware component diagnostics
  monitoring  - System performance monitoring  
  packages    - Package management (Windows only)

Interface Options:
  --cli       - Command Line Interface (default)
  --gui       - Graphical User Interface
  --web       - Web Browser Interface

Examples:
  python main.py --cli battery
  python main.py --gui
  python main.py --web --port 8080
        '''
    )
    
    # Interface selection
    interface_group = parser.add_mutually_exclusive_group()
    interface_group.add_argument('--cli', action='store_true', default=True,
                                help='Use Command Line Interface (default)')
    interface_group.add_argument('--gui', action='store_true',
                                help='Use Graphical User Interface')
    interface_group.add_argument('--web', action='store_true',
                                help='Use Web Browser Interface')
    
    # Web interface options
    parser.add_argument('--port', type=int, default=8080,
                       help='Port for web interface (default: 8080)')
    parser.add_argument('--host', default='localhost',
                       help='Host for web interface (default: localhost)')
    
    # Tool selection (for CLI)
    parser.add_argument('tool', nargs='?', 
                       choices=['battery', 'diagnostics', 'monitoring', 'packages'],
                       help='Tool to run (CLI only)')
    
    # General options
    parser.add_argument('--config', 
                       help='Path to configuration file')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    
    args = parser.parse_args()
    
    # Configure logging
    if args.verbose:
        logger.set_level('DEBUG')
    
    # Load configuration
    if args.config:
        config.load_from_file(args.config)
    
    logger.info("Starting All-in-One System Tools")
    
    try:
        # Launch appropriate interface
        if args.gui:
            logger.info("Launching GUI interface")
            interface = GUIInterface(config, logger)
            interface.run()
            
        elif args.web:
            logger.info(f"Launching web interface on {args.host}:{args.port}")
            interface = WebInterface(config, logger)
            interface.run(host=args.host, port=args.port)
            
        else:  # CLI (default)
            logger.info("Launching CLI interface")
            interface = CLIInterface(config, logger)
            interface.run(args.tool)
            
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application error: {e}")
        if args.verbose:
            logger.exception("Full traceback:")
        sys.exit(1)

if __name__ == "__main__":
    main()
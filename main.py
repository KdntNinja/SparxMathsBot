#!/usr/bin/env python3
"""
Main entry point for SparxMathsBot.

This script can be run directly to start the bot.
"""

import argparse
import sys
from sparx_maths_bot import SparxMathsBot


def main():
    """Main function to run the SparxMathsBot."""
    parser = argparse.ArgumentParser(
        description="SparxMathsBot - Automate Sparx maths homework",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "-u", "--username",
        type=str,
        help="Sparx account username"
    )
    
    parser.add_argument(
        "-p", "--password", 
        type=str,
        help="Sparx account password"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="SparxMathsBot 0.1.0"
    )
    
    args = parser.parse_args()
    
    # Create and run the bot
    bot = SparxMathsBot(username=args.username, password=args.password)
    bot.run()


if __name__ == "__main__":
    main()
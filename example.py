#!/usr/bin/env python3
"""
Example script demonstrating how to use SparxMathsBot.

This is a simple example showing basic usage patterns.
"""

from sparx_maths_bot import SparxMathsBot


def main():
    """Example usage of SparxMathsBot."""
    print("SparxMathsBot Example")
    print("=" * 20)
    
    # Create bot instance
    print("Creating bot instance...")
    bot = SparxMathsBot()
    
    # You can also pass credentials directly:
    # bot = SparxMathsBot(username="your_username", password="your_password")
    
    print(f"Bot version: {bot.__class__.__module__}")
    print("Bot created successfully!")
    
    # Example of setting credentials after initialization
    bot.username = "example_user"
    bot.password = "example_password"
    
    print(f"Username set to: {bot.username}")
    print("Note: Password is stored securely (not displayed)")
    
    print("\nTo actually run the bot, use:")
    print("python main.py --username YOUR_USERNAME --password YOUR_PASSWORD")
    print("\nOr run as a module:")
    print("python -m sparx_maths_bot --username YOUR_USERNAME --password YOUR_PASSWORD")


if __name__ == "__main__":
    main()
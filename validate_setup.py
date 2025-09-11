#!/usr/bin/env python3
"""
Validation script to check SparxMathsBot installation and setup.

Run this script to verify that SparxMathsBot is properly installed and configured.
"""

import sys
import importlib.util


def check_python_version():
    """Check if Python version is supported."""
    min_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version >= min_version:
        print(f"✅ Python version: {sys.version.split()[0]} (supported)")
        return True
    else:
        print(f"❌ Python version: {sys.version.split()[0]} (requires >= {min_version[0]}.{min_version[1]})")
        return False


def check_package_import():
    """Check if the sparx_maths_bot package can be imported."""
    try:
        import sparx_maths_bot
        print(f"✅ Package import: sparx_maths_bot v{sparx_maths_bot.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Package import failed: {e}")
        return False


def check_dependencies():
    """Check if required dependencies are available."""
    dependencies = ["requests", "beautifulsoup4", "selenium"]
    all_good = True
    
    for dep in dependencies:
        spec = importlib.util.find_spec(dep)
        if spec is not None:
            print(f"✅ Dependency: {dep}")
        else:
            print(f"❌ Missing dependency: {dep}")
            all_good = False
    
    return all_good


def check_bot_functionality():
    """Check if bot can be instantiated."""
    try:
        from sparx_maths_bot import SparxMathsBot
        bot = SparxMathsBot()
        print("✅ Bot instantiation: successful")
        return True
    except Exception as e:
        print(f"❌ Bot instantiation failed: {e}")
        return False


def main():
    """Run all validation checks."""
    print("SparxMathsBot Setup Validation")
    print("=" * 30)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Package Import", check_package_import),
        ("Dependencies", check_dependencies),
        ("Bot Functionality", check_bot_functionality),
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"Checking {check_name}...")
        result = check_func()
        if not result:
            all_passed = False
        print()
    
    print("=" * 30)
    if all_passed:
        print("🎉 All checks passed! SparxMathsBot is ready to use.")
        print("\nGet started with:")
        print("  python main.py --help")
        print("  python -m sparx_maths_bot --help")
    else:
        print("❌ Some checks failed. Please review the issues above.")
        print("\nTo install dependencies, run:")
        print("  pip install -r requirements.txt")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
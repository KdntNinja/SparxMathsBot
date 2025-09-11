# SparxMathsBot

A Python bot to automate Sparx maths homework tasks.

## Features

- 🤖 Automated homework solving
- 📚 Educational automation tool
- 🔐 Secure login handling
- 📊 Progress tracking

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Development Installation

```bash
pip install -e .[dev]
```

## Usage

### Basic Usage

```bash
python main.py --username your_username --password your_password
```

### Using as a Python Module

```python
from sparx_maths_bot import SparxMathsBot

# Create bot instance
bot = SparxMathsBot(username="your_username", password="your_password")

# Run the bot
bot.run()
```

### Command Line Options

```
usage: main.py [-h] [-u USERNAME] [-p PASSWORD] [--version]

SparxMathsBot - Automate Sparx maths homework

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Sparx account username
  -p PASSWORD, --password PASSWORD
                        Sparx account password
  --version             show program's version number and exit
```

## Project Structure

```
SparxMathsBot/
├── sparx_maths_bot/          # Main package
│   ├── __init__.py           # Package initialization
│   └── bot.py                # Core bot implementation
├── main.py                   # Main entry point
├── pyproject.toml           # Project configuration
├── requirements.txt         # Dependencies
├── README.md               # This file
├── LICENSE                 # MIT License
└── .gitignore             # Git ignore rules
```

## Development

### Code Style
This project uses `black` for code formatting and `flake8` for linting.

### Testing
Run tests with pytest:
```bash
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational purposes only. Please ensure compliance with your institution's academic integrity policies.

# SparxMathsBot

This is a bot to automate sparx maths homework.

## Project Structure

This project has been modularized for better organization and future expansion. Here's the breakdown of the structure:

## Directory Structure

```files
SparxMathsBot/
├── main.py                    # Main entry point
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── build/                     # Auto-managed directory for binaries (geckodriver, firefox)
└── src/                       # Source code package
    ├── __init__.py            # Package initialization
    ├── config.py              # Configuration constants and settings
    ├── logging_utils.py       # Logging setup and decorators
    ├── browser_manager.py     # Browser automation utilities
    ├── image_processor.py     # OCR and image processing
    ├── email_notifier.py      # Email notification service
    ├── geckodriver_setup.py   # Automatic geckodriver/firefox setup
    └── workflow.py            # Main workflow implementation
```

## Module Descriptions

### `main.py`

- Entry point for the application
- Handles geckodriver setup and logging initialization
- Runs the main workflow

### `src/config.py`

- Contains all configuration constants
- Coordinate locations, CSS selectors, XPaths
- Quiz settings and thresholds

### `src/logging_utils.py`

- Logging configuration and setup
- Function call decorator for debugging
- Centralized logger management

### `src/browser_manager.py`

- Browser initialization and management
- WebDriver utilities and element waiting
- Screenshot capture functionality

### `src/image_processor.py`

- OCR operations using both pytesseract and EasyOCR
- Image cropping and processing
- Pattern matching for multiplication problems

### `src/email_notifier.py`

- Email notification service using Resend
- Sends completion notifications with logs
- Error handling for email failures

### `src/geckodriver_setup.py`

- Automatic download and setup of geckodriver
- Automatic download and setup of Firefox browser
- Manages binaries in build/ directory

### `src/workflow.py`

- Main workflow implementation
- Orchestrates all components
- Handles school selection, login, navigation, and quiz solving

## Benefits of This Structure

1. **Modularity**: Each component has a specific responsibility
2. **Maintainability**: Easy to locate and modify specific functionality
3. **Testability**: Components can be tested independently
4. **Extensibility**: New features can be added as separate modules
5. **Reusability**: Components can be reused in other projects

## Future Expansion

This structure makes it easy to add new features:

- Additional question types (new modules in `src/`)
- Different notification methods (extend `email_notifier.py`)
- Alternative OCR engines (extend `image_processor.py`)
- Multiple browser support (extend `browser_manager.py`)
- Configuration file support (extend `config.py`)

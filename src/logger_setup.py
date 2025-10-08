import logging
import os

def setup_logger(name: str = "SparxTTWorkflow", log_file: str = "workflow_log.txt") -> logging.Logger:
    """Set up and configure logger."""
    # Create build directory if it doesn't exist
    build_dir = "build"
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    
    log_file_path = os.path.join(build_dir, log_file)
    
    log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_file_path, mode="w")
    
    console_handler.setFormatter(log_formatter)
    file_handler.setFormatter(log_formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

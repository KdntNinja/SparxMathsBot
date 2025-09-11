"""Configuration and constants for SparxMathsBot."""

# Coordinate constants
START_BUTTON_LOCATION = (958, 914)
CROPPED_IMAGE_BOX = (724, 139, 1205, 215)  # (left, upper, right, lower)

# CSS selectors and XPaths
SCHOOL_INPUT_CLASS_NAME = "SCHOOL_INPUT_CLASS_NAME"  # From environment
USERNAME_ID = "username"
PASSWORD_ID = "password"
LOGIN_BUTTON_CLASS_NAME = "sm-button login-button"
HOMEWORK_TEXT_CLASS_NAME = "_PackageLeft_s1pvn_28"
START_BUTTON_XPATH = "//a[contains(@class, '_Task_1p2y5_1')]//div[contains(@class, '_TaskChip_1p2y5_79') and text()='Start']"
TIMES_TABLES_TEXT_XPATH = "//span[contains(text(), 'Times Tables')]"
CLUB_CHECK_TEXT_XPATH = (
    "//div[contains(@class, '_Content_nt2r3_194') and text()='100 Club Check']"
)
TIMES_TABLES_EXIT_XPATH = "//a[contains(@class, '_BackButton_1iso5_1')]"

# URLs
SCHOOL_URL = "https://selectschool.sparxmaths.uk/?forget=1"

# Quiz settings
MAX_ATTEMPTS = 60
INTERMEDIATE_CHECKPOINTS = [25, 50]

from pathlib import Path


class Constants:
    # Base directory of the add-on
    BASE_DIR = Path(__file__).parent

    # File paths
    DB_PATH = BASE_DIR / 'user_files' / 'database.db'
    JSON_FILENAME = '_hanzihome.json'
    # This is the path to the JSON file containing the character information
    JSON_PATH = BASE_DIR / 'user_files' / JSON_FILENAME
    SQL_PATH = BASE_DIR /  'create_tables.sql'
    JS_FILENAME = '_hanzihome.js'
    # Useful javascript functions used in the webview
    JS_PATH = BASE_DIR / JS_FILENAME


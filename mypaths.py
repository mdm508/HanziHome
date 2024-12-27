from pathlib import Path


class Constants:
    # Base directory of the add-on
    BASE_DIR = Path(__file__).parent

    # File paths
    DB_PATH = BASE_DIR / 'user_files' / 'database.db'
    JSON_FILENAME = '_hanzihome.json'
    JSON_PATH = BASE_DIR / 'user_files' / JSON_FILENAME
    SQL_PATH = BASE_DIR /  'create_tables.sql'
    JS_FILENAME = '_hanzihome.js'
    JS_PATH = BASE_DIR / JS_FILENAME


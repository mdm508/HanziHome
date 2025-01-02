import shutil
import os
from pathlib import Path

from aqt import mw
from aqt.utils import showInfo

try:
    # Anki imports (for deployment inside Anki)
    from .mypaths import Constants
except ImportError:
    from mypaths import Constants



def _copy_file_to_media(source: Path, filename: str):
    """
    Copies a file to the collection.media folder.
    Args:
        source (Path): The source file path.
        filename (str): The name of the file in the destination folder.
    Note: To get anki mobile to sync these media files we need to delete them.
    """
    try:
        # Define destination path
        dest = Path(mw.col.media.dir()) / filename
        # Check if the file exists
        if os.path.exists(dest):
            # Delete the file
            os.remove(dest)
            print(f"File '{dest}' has been deleted successfully.")
        # Copy the file
        shutil.copy2(source, dest)
        showInfo(f"Copied {filename} to: {dest}")
    except FileNotFoundError:
        showInfo(f"Source file not found: {source}")
    except Exception as e:
        showInfo(f"Failed to copy {filename}: {str(e)}")

def copy_json_to_media_folder():
    _copy_file_to_media(Constants.JSON_PATH, Constants.JSON_FILENAME)

def copy_resources_to_media_folder():
    """
    Copies required JSON and JavaScript files to collections.media folder
    for mobile compatibility.
    """
    from .mypaths import Constants
    # Copy JSON file
    copy_json_to_media_folder()
    # Copy JavaScript file
    _copy_file_to_media(Constants.JS_PATH, Constants.JS_FILENAME)
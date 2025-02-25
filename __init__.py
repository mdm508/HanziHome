from aqt import gui_hooks
from aqt.qt import *
from aqt import QAction, QWidget
from bs4 import BeautifulSoup
from aqt import mw
from aqt import dialogs
from aqt.webview import AnkiWebView
from aqt.utils import showInfo

from .helpers import copy_resources_to_media_folder, config_exists
from .dbcontroller import DatabaseController
from .viewer import HanziViewer
from .config import has, get

CON = DatabaseController()



def add_hanzi_info_to_template(card_layout):
    """
        Checks both the question and answer sides of the card for a div tag with id=hanzihome.
        If found, it will add JavaScript and HTML required to show info about each character in the 'hanzi' field.
        :param card_layout:
        :return:
        """
    # Check both question and answer templates
    for side in ["qfmt", "afmt"]:
        html = card_layout.current_template()[side]
        soup = BeautifulSoup(html, "html.parser")
        home_div = soup.find("div", {"id": "hanzihome"})
        if home_div:
            # Found the div, proceed with customization
            copy_resources_to_media_folder()
            # Use hanziSource field... look up each character in the JSON
            return
    # If no div is found in either template
    showInfo("Could not find div with id='hanzihome' in question or answer template.")
    #using hanziSource field...look up each character in the json


def add_custom_button_to_card_layout(card_layout):
    # Create the button
    btn = QPushButton("Add Hanzi Info")
    btn.clicked.connect(lambda: add_hanzi_info_to_template(card_layout))
    # Add the button to the bottom buttons area
    card_layout.buttons.addWidget(btn)  # `buttons` is already a QHBoxLayout

def on_lookup_hanzi(selected_text, db: DatabaseController):
    # Replace this with your Hanzi lookup function or URL
    mw.hanzi_viewer = v = HanziViewer(selected_text, db)
    v.show()

def on_webview_will_show_context_menu(webview: AnkiWebView, menu: QMenu):
    # Ensure we're only modifying the main reviewer's context menu
    if getattr(webview, "title", "") != "main webview":
        return

    # Get selected text and add an option if text is present
    selected_text = webview.selectedText().strip()
    if selected_text:
        action = QAction("Look up Hanzi", webview)
        action.triggered.connect(lambda: on_lookup_hanzi(selected_text, CON))
        menu.addAction(action)

### Search related in browser
def raise_window(window: QWidget):
    window.setWindowState(
        (window.windowState() & ~Qt.WindowState.WindowMinimized)
        | Qt.WindowState.WindowActive
    )
    window.raise_()
    window.activateWindow()

def open_browser(text: str):
    browser = dialogs.open("Browser", mw)
    # Get infro from 
    deck = get('deck')
    hanzi_field_name = get('hanziFieldName')
    text = f"deck:{deck} {hanzi_field_name}:{text}"
    browser.form.searchEdit.lineEdit().setText(text)
    browser.onSearchActivated()
    # For newer Anki versions:
    dialogs.open('Browser', mw, search=(text,))
    #raise_window(browser)


def webview_search_collection(web_view):
    text = web_view.selectedText()
    open_browser(text)

def on_webview_context_menu(webview, menu):
    collection_action = menu.addAction("Search Hanzi in Deck")
    collection_action.triggered.connect(lambda: webview_search_collection(webview))


def editor_field_focused(note, current_field_idx):
    print(note)
    print(current_field_idx)



def main():
    # Register the 'web/' folder for external access
    mw.addonManager.setWebExports(__name__, r"web/.*(css|js)")
    if not config_exists():
        copy_resources_to_media_folder()
        print("Config file created.")
    else:
        print("Config file already exists.")
    gui_hooks.webview_will_show_context_menu.append(on_webview_context_menu)
    gui_hooks.editor_will_show_context_menu.append(on_webview_context_menu)
    



main()
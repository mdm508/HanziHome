import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from aqt import mw
from aqt.operations import QueryOp

from .dbcontroller import DatabaseController

class HanziViewer(QWidget):
    def __init__(self, search_char:str, db: DatabaseController, parent=None):
        super().__init__(parent)
        self.data = None
        self.search_char = search_char
        self.con = db
        self.setWindowTitle("Hanzi Viewer")
        self.setFixedSize(600, 420)  # Increased window height
        self.fetch_data()
        self.init_ui()
    # Initialize UI Components

    def fetch_data(self):
        self.data = self.con.fetch_from_json(self.search_char)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        if data:
            # Set background color
            self.setStyleSheet("background-color: white;")
            # Keyword Section
            layout.addLayout(self._create_keyword_section())
            # Hanzi and Info Section
            layout.addLayout(self._create_hanzi_info_section())
            # Table Section
            layout.addWidget(self._create_table_section())
            # Buttons Section
            layout.addLayout(self._create_buttons_section())
            self.setLayout(layout)
        else:
            # Show 'No Results' label if no data is fetched
            no_results_label = QLabel("No results found.")
            no_results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_results_label.setStyleSheet("font-size: 16pt; color: red;")
            layout.addWidget(no_results_label)

    # Keyword Section
    def _create_keyword_section(self):
        keyword_layout = QHBoxLayout()
        keyword_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Keyword Label
        keyword_label = QLabel("Keyword:")
        keyword_label.setStyleSheet("font-size: 14pt;")

        # Keyword Input
        self.keyword_input = QLineEdit(self.data.get("keyword", ""))
        self.keyword_input.setFixedWidth(300)
        self.keyword_input.setReadOnly(True)
        self.keyword_input.setStyleSheet("font-size: 14pt;")

        # Buttons
        self.edit_button = QPushButton("Edit")
        self.edit_button.setStyleSheet("font-size: 12pt;")
        self.edit_button.clicked.connect(self._enable_edit)

        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet("font-size: 12pt;")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self._save_keyword)

        # Add to layout
        keyword_layout.addWidget(keyword_label)
        keyword_layout.addWidget(self.keyword_input)
        keyword_layout.addWidget(self.edit_button)
        keyword_layout.addWidget(self.save_button)

        return keyword_layout

    # Hanzi and Info Section
    def _create_hanzi_info_section(self):
        section_layout = QHBoxLayout()
        section_layout.addWidget(self._create_hanzi_display())
        section_layout.addWidget(self._create_zhuyin_display())
        section_layout.addLayout(self._create_info_layout())
        return section_layout

    def _create_hanzi_display(self):
        hanzi_label = QLabel(self.data.get("character", ""))
        hanzi_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hanzi_label.setStyleSheet("font-size: 60pt; font-weight: bold;")
        return hanzi_label

    def _create_zhuyin_display(self):
        zhuyin_display = QLabel(", ".join(self.data.get("zhuyin", [])))
        zhuyin_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        zhuyin_display.setStyleSheet("font-size: 14pt;")
        return zhuyin_display

    def _create_info_layout(self):
        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Decomposition
        decomp_label = QLabel(f"Decomposition: {self.data.get('decomposition', '')}")
        decomp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        decomp_label.setStyleSheet("font-size: 14pt;")
        info_layout.addWidget(decomp_label)

        # Radical
        radical_label = QLabel(f"Radical: {self.data.get('radical', '')}")
        radical_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        radical_label.setStyleSheet("font-size: 14pt;")
        info_layout.addWidget(radical_label)

        return info_layout

    # Table Section
    def _create_table_section(self):
        table = QTableWidget(0, 2)
        table.setHorizontalHeaderLabels(["Field", "Value"])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.horizontalHeader().setStretchLastSection(True)
        table.setStyleSheet("font-size: 12pt;")

        # Populate Table
        self._add_table_row(table, "Definition", self.data.get("definition", ""))
        self._add_table_row(table, "Pinyin", ", ".join(self.data.get("pinyin", [])))
        self._add_table_row(table, "IPA", ", ".join(self.data.get("ipa", [])))

        etymology = self.data.get("etymology", {})
        for key, value in etymology.items():
            self._add_table_row(table, f"Etymology ({key})", value)

        return table

    # Add Rows to Table
    def _add_table_row(self, table, field, value):
        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, 0, QTableWidgetItem(str(field)))
        table.setItem(row, 1, QTableWidgetItem(str(value)))

    # Buttons Section
    def _create_buttons_section(self):
        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        close_button = QPushButton("Close")
        close_button.setStyleSheet("font-size: 12pt;")
        close_button.clicked.connect(self.close)
        buttons_layout.addWidget(close_button)
        return buttons_layout

    # Enable Editing
    def _enable_edit(self):
        self.keyword_input.setReadOnly(False)
        self.save_button.setEnabled(True)

    def _disable_edit(self):
        # success handler for save keyword
        # restores stuff input and save buttons
        self.keyword_input.setReadOnly(True)
        self.save_button.setEnabled(False)

    from aqt import mw  # Import mw to detect Anki environment

    def _save_keyword(self):
        new_keyword = self.keyword_input.text()
        try:
            # Update the database directly in the main thread
            self.con.update_keyword(new_keyword, self.data.get("character", ""))
            print(f"Keyword saved: {new_keyword}")
        except Exception as e:
            print(f"Failed to save keyword: {e}")
        finally:
            # Update UI in the main thread
            self._disable_edit()


# Example Data
data = {
    "character": "頓",
    "definition": "to pause; to bow; to arrange",
    "decomposition": "\u2ff0屯頁",
    "radical": "頁",
    "keyword": "pause",
    "pinyin": ["d\u00f9n"],
    "ipa": ["tw\u0252n\u02e5\u02e9"],
    "zhuyin": ["ㄉㄨㄣˋ"],
    "etymology": {
        "type": "pictophonetic",
        "hint": "head",
        "phonetic": "屯",
        "semantic": "頁",
    },
}

# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = HanziViewer("頓", DatabaseController())
    viewer.show()
    sys.exit(app.exec())

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from .dbcontroller import DatabaseController

class HanziViewer(QWidget):
    window_count = 0
    def __init__(self, search_char:str, db: DatabaseController, parent=None):
        super().__init__(parent)
        HanziViewer.window_count += 1
        self.search_char = search_char
        self.con = db
        self.setFixedSize(600, 420)  # Increased window height
        self.data = self.fetch_data()
        self.init_ui()
    # Initialize UI Components

    # default to search character obtained from user clicking on context menu
    # if char is present search using that
    def fetch_data(self, char=None):
        if char:
            search_char = char
        else:
            search_char = self.search_char

        return self.con.fetch_from_json(search_char)

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
            self.setWindowTitle(f"Win {HanziViewer.window_count} {self.search_char}")
        else:
            # Show 'No Results' label if no data is fetched
            no_results_label = QLabel("No results found.")
            no_results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_results_label.setStyleSheet("font-size: 16pt; color: red;")
            layout.addWidget(no_results_label)
            self.setWindowTitle(f"Win {HanziViewer.window_count} No Results for {self.search_char}")

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

    # Setup widget with a horizontal layout
    def _create_horizontal_layout_widget(self):
        hlayout = QHBoxLayout()
        hlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Create a container widget for the layout
        widget = QWidget()
        widget.setLayout(hlayout)  # Set the layout on the widget
        return widget


    def _create_info_layout(self):
        info_layout = QVBoxLayout()
        info_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self._create_radical_layout())
        info_layout.addWidget(self._create_decomposition_layout())

        return info_layout

    # Makes a searchable radical
    def _create_radical_layout(self):
        radical_widget = self._create_horizontal_layout_widget()
        radical = self.data.get('radical', '')
        radical_label = QLabel(f"Radical: {radical}")
        self._make_searchable_label(radical, radical_label)
        radical_widget.layout().addWidget(radical_label)
        return radical_widget

    # makes searchable decomposition labels
    def _create_decomposition_layout(self):
        decomp_widget = self._create_horizontal_layout_widget()
        # Process decomposition characters
        decomposition = self.data.get("decomposition", "")
        for char in decomposition:
            # Only process Chinese characters
            decomp_label = self._make_searchable_label(char)
            decomp_widget.layout().addWidget(decomp_label)
        # Return the widget containing the layout
        return decomp_widget

    # return a searchable label for the give character.
    #  ptionally pass in their own label
    # if not one is created for you.
    def _make_searchable_label(self, char, label=None):
        if not label:
            label = QLabel(char)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 14pt")
        if self._in_db(char):
            label.setStyleSheet("font-size: 14pt; color: blue;")
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            label.mousePressEvent = lambda event, c=char: self._open_new_viewer(c)
        return label
    # true if character data exists
    def _in_db(self,char):
        response = self.fetch_data(char)
        return bool(response)

    def _open_new_viewer(self, char):
        new_viewer = HanziViewer(char, self.con)
        new_viewer.show()

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

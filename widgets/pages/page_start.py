from script.utils import get_default_game_path
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QLineEdit,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
import os


class PageStart(QWidget):
    feed_finish: Signal = Signal(bool)

    def __init__(self):
        super().__init__()

        # create layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout_browse_game = QHBoxLayout()
        layout_browse_atm = QHBoxLayout()

        # create widgets
        label_description = QLabel(
            "You can select community presets and choose what you want to merge into your atmosphere config file.")
        label_description.setStyleSheet("font-size: 12pt; font-weight: 100")
        label_description.setWordWrap(True)
        label_description.setAlignment(Qt.AlignmentFlag.AlignJustify)

        # Default ini
        label_default_ini = QLabel("Select the default atmosphere")
        label_default_ini.setStyleSheet("font-size: 12pt; font-weight: 100")
        label_default_ini.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.browse_default_input = QLineEdit(get_default_game_path())
        self.browse_default_button = QPushButton("Browse")

        # Community ini
        label_community_ini = QLabel("Select the atmosphere you want to merge")
        label_community_ini.setStyleSheet("font-size: 12pt; font-weight: 100")
        label_community_ini.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.browse_community_input = QLineEdit()
        self.browse_community_button = QPushButton("Browse")

        # Feed
        self.feed_button = QPushButton("Load files")

        # add widgets
        layout.addWidget(label_description)
        layout.addSpacing(15)

        layout.addWidget(label_default_ini)
        layout_browse_game.addWidget(self.browse_default_input)
        layout_browse_game.addWidget(self.browse_default_button)
        layout.addLayout(layout_browse_game)

        layout.addSpacing(10)

        layout.addWidget(label_community_ini)
        layout_browse_atm.addWidget(self.browse_community_input)
        layout_browse_atm.addWidget(self.browse_community_button)
        layout.addLayout(layout_browse_atm)

        layout.addSpacing(15)
        layout.addWidget(self.feed_button)

        self.setLayout(layout)

        # Connect functions
        self.feed_button.clicked.connect(self.click_feed)
        self.browse_default_button.clicked.connect(
            lambda: self.browse_atmospheres(
                is_community=False,
                browse_input=self.browse_default_input
            )
        )
        self.browse_community_button.clicked.connect(
            lambda: self.browse_atmospheres(
                is_community=True,
                browse_input=self.browse_community_input
            )
        )

    def browse_atmospheres(self, is_community: bool, browse_input: QLineEdit) -> None:
        HOME = os.path.expanduser("~")
        label: str = ""

        if is_community:
            label = "Select Community Atmosphere"
        else:
            label = "Select Original Atmosphere"

        file_selection: tuple[str, str] = QFileDialog.getOpenFileName(
            self,
            label,
            HOME,
            "INI Files (*.ini)"
        )

        file_path = file_selection[0]

        if file_path:
            browse_input.setText(file_path)

    def click_feed(self) -> None:
        if self.browse_default_input.text() and self.browse_community_input.text():
            self.feed_finish.emit(True)
        else:
            self.feed_finish.emit(False)

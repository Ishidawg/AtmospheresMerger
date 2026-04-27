from typing import Any
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget
)
import configparser

from script.utils import run_merge


class PageMerge(QWidget):
    def __init__(self):
        super().__init__()

        self.game_path: str = ""
        self.community_path: str = ""
        self.checkboxes: list[Any] = []

        # create layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # create widgets
        label_description = QLabel("Select atmospheres you want to merge.")
        label_description.setStyleSheet("font-size: 12pt; font-weight: 100")
        label_description.setWordWrap(True)

        # Scroll area (even better than LeShade)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()

        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.scroll_content)

        self.btn_install = QPushButton("Merge atmospheres")
        self.btn_install.setEnabled(False)

        # Filter buttons
        self.btn_select_all = QPushButton("Select All")
        self.btn_deselect_all = QPushButton("Deselect All")
        self.filter_layout = QHBoxLayout()

        self.filter_layout.addWidget(self.btn_select_all)
        self.filter_layout.addWidget(self.btn_deselect_all)

        # add widgets
        layout.addWidget(label_description)
        layout.addSpacing(10)
        layout.addWidget(self.scroll_area)
        layout.addSpacing(10)
        layout.addLayout(self.filter_layout)
        layout.addSpacing(5)
        layout.addWidget(self.btn_install)
        self.setLayout(layout)

        # Connect functions
        self.btn_install.clicked.connect(self.start_merge)
        self.btn_select_all.clicked.connect(self.select_all)
        self.btn_deselect_all.clicked.connect(self.deselect_all)

    def select_all(self) -> None:
        for cb in self.checkboxes:
            cb.setChecked(True)

    def deselect_all(self) -> None:
        for cb in self.checkboxes:
            cb.setChecked(False)

    def load_atmospheres(self, game_path: str, community_path: str) -> None:
        self.game_path = game_path
        self.community_path = community_path

        for cb in self.checkboxes:
            self.scroll_layout.removeWidget(cb)
            cb.deleteLater()

        self.checkboxes.clear()

        config: configparser.ConfigParser = configparser.ConfigParser()

        try:
            config.read(community_path, encoding='utf-8')
            sections: list[Any] = config.sections()

            if not sections:
                QMessageBox.warning(self, "Invalid File",
                                    "No atmospheres found.")
                self.btn_install.setEnabled(False)
                return

            for section in sections:
                if section == "Atmosphere_Triggers" or section.startswith("level_"):
                    continue

                cb = QCheckBox(section)
                self.scroll_layout.addWidget(cb)
                self.checkboxes.append(cb)

            self.btn_install.setEnabled(True)
        except Exception as e:
            QMessageBox.warning(self, "Load Error",
                                f"Could not load sections:\n{str(e)}")
            self.btn_install.setEnabled(False)

    def start_merge(self) -> None:
        selected: list[str] = [cb.text()
                               for cb in self.checkboxes if cb.isChecked()]

        if not selected:
            QMessageBox.warning(
                self,
                "No atmosphered selected",
                "Please check at least one atmosphere."
            )
            return

        run_merge(self, self.game_path, self.community_path, selected)

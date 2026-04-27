from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget
)
from enum import IntEnum
import sys

from widgets.pages.page_start import PageStart
from widgets.pages.page_merge import PageMerge
from widgets.widget_bottom_buttons import WidgetBottomButtons
from widgets.widget_title import WidgetTitle


class Pages(IntEnum):
    START = 0
    MERGE = 1


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        WINDOW_SIZE: list[int] = [560, 650]
        WINDOW_TITLE: str = "Atmosphere Merger"

        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(WINDOW_SIZE[0], WINDOW_SIZE[1])

        WIDGET_MAIN = QWidget()
        self.setCentralWidget(WIDGET_MAIN)
        self.layout_main = QVBoxLayout(WIDGET_MAIN)

        self.stack = QStackedWidget()
        self.stack.setContentsMargins(20, 0, 20, 0)

        self.action_button: WidgetBottomButtons = WidgetBottomButtons()
        self.page_start: PageStart = PageStart()
        self.page_merge: PageMerge = PageMerge()

        self.pages: list[QWidget] = [
            self.page_start,
            self.page_merge
        ]

        for page in self.pages:
            self.stack.addWidget(page)

        # Add Wigdets
        self.layout_main.addWidget(WidgetTitle())
        self.layout_main.addWidget(self.stack)
        self.layout_main.addWidget(self.action_button)

        # Connect signals
        self.page_start.feed_finish.connect(self.handle_files)
        self.action_button.btn_next.clicked.connect(self.switch_to_merge_page)

    def handle_files(self, succcess: bool) -> None:
        if succcess:
            self.action_button.btn_next.setEnabled(True)

    def switch_to_merge_page(self) -> None:
        game_path: str = self.page_start.browse_default_input.text()
        community_path: str = self.page_start.browse_community_input.text()

        self.page_merge.load_atmospheres(game_path, community_path)

        self.stack.setCurrentIndex(Pages.MERGE)

        # Copied from update_next_button (LeShade)
        self.action_button.btn_next.setText("Close")
        self.action_button.btn_next.clicked.disconnect()
        self.action_button.btn_next.clicked.connect(self.close)


def main() -> None:
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

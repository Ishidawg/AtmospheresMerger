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

        self.pages: list[QWidget] = [
            self.page_start,
        ]

        for page in self.pages:
            self.stack.addWidget(page)

        # Add Wigdets
        self.layout_main.addWidget(WidgetTitle())
        self.layout_main.addWidget(self.stack)
        self.layout_main.addWidget(self.action_button)

        # Connect signals
        self.page_start.feed_finish.connect(self.handle_files)

    def handle_files(self, succcess: bool) -> None:
        if succcess:
            self.action_button.btn_next.setEnabled(True)
            self.action_button.btn_next.show()
        else:
            self.action_button.btn_next.hide()


def main() -> None:
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

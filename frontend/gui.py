import sys
import requests
import threading
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QScrollArea, QFrame, QGridLayout
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class HistomendApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Histomend - Your AI Documentary Buddy")

        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(int(screen.width() * 0.05), int(screen.height() * 0.05),
                         int(screen.width() * 0.9), int(screen.height() * 0.85))

        self.main_layout = QVBoxLayout()
        self.create_search_bar()
        self.create_results_area()
        self.setLayout(self.main_layout)

    def create_search_bar(self):
        self.search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter a historical topic...")
        self.search_input.setFixedHeight(40)

        self.search_button = QPushButton("Search")
        self.search_button.setFixedHeight(40)

        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_button)

        self.main_layout.addLayout(self.search_layout)
        self.search_button.clicked.connect(self.get_suggestions)

    def create_results_area(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.results_container = QWidget()
        self.results_layout = QGridLayout()
        self.results_layout.setSpacing(20)

        self.results_container.setLayout(self.results_layout)
        self.scroll_area.setWidget(self.results_container)

        self.main_layout.addWidget(self.scroll_area)

    def get_suggestions(self):
        topic = self.search_input.text()
        response = requests.post("http://127.0.0.1:5000/suggest", json={"query": topic})

        # Clear previous results
        for i in reversed(range(self.results_layout.count())):
            widget = self.results_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        if response.status_code == 200:
            data = response.json()
            for index, vid in enumerate(data["suggestions"]):
                self.display_result(index, vid)
        else:
            error_label = QLabel("Error retrieving suggestions.")
            self.results_layout.addWidget(error_label)

    def display_result(self, index, vid):
        title, description, thumbnail_url, video_url = vid

        container = QFrame()
        container.setFrameShape(QFrame.Box)
        container.setLineWidth(1)
        layout = QVBoxLayout()

        # Thumbnail
        thumb = QLabel()
        thumb.setFixedSize(320, 180)
        thumb.setCursor(Qt.PointingHandCursor)

        try:
            response = requests.get(thumbnail_url)
            response.raise_for_status()
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            thumb.setPixmap(pixmap.scaled(320, 180, Qt.KeepAspectRatio))
        except Exception as e:
            thumb.setText("Image Load Error")
            print("Image Load Error:", e)

        # Open in browser using thread
        def open_video():
            webbrowser.open_new_tab(video_url)

        thumb.mousePressEvent = lambda e: threading.Thread(target=open_video).start()
        layout.addWidget(thumb)

        # Title label
        title_label = QLabel(f"<u>{title}</u>")
        title_label.setStyleSheet("color: #1a73e8;")
        title_label.setCursor(Qt.PointingHandCursor)
        title_label.mousePressEvent = lambda e: threading.Thread(target=open_video).start()
        layout.addWidget(title_label)

        # Description
        desc = QLabel(description)
        desc.setWordWrap(True)
        layout.addWidget(desc)

        container.setLayout(layout)
        self.results_layout.addWidget(container, index // 2, index % 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HistomendApp()
    window.show()
    sys.exit(app.exec_())

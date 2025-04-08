import sys
import json
import requests
from io import BytesIO
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QListWidget, QListWidgetItem, QTextBrowser)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QFile, QTextStream
from user_profile import load_user_data, update_search_history


class HistomendDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Histomend - Fantasy Dashboard")
        self.setGeometry(200, 100, 1000, 600)
        self.apply_theme()

        self.user_data = load_user_data()
        self.init_ui()

    def apply_theme(self):
        file = QFile("frontend/styles/theme.qss")  # Adjust path if needed
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

    def init_ui(self):
        main_layout = QVBoxLayout()

        # User Panel
        user_panel = QHBoxLayout()
        self.username_label = QLabel(f"Welcome, {self.user_data['username']} 🧙‍♂️")
        self.username_label.setFont(QFont("Consolas", 14))
        user_panel.addWidget(self.username_label)
        user_panel.addStretch()

        # Search Bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for educational videos...")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.perform_search)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        # Video Results
        self.results_list = QListWidget()

        # Stats Panel
        stats_layout = QHBoxLayout()
        self.stats_label = QLabel(self.format_stats())
        self.stats_label.setFont(QFont("Consolas", 10))
        stats_layout.addWidget(self.stats_label)
        stats_layout.addStretch()

        main_layout.addLayout(user_panel)
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.results_list)
        main_layout.addLayout(stats_layout)
        self.setLayout(main_layout)

    def perform_search(self):
        query = self.search_input.text().strip()
        if not query:
            return

        update_search_history(query)
        self.user_data = load_user_data()
        self.stats_label.setText(self.format_stats())
        self.results_list.clear()

        try:
            response = requests.post("http://127.0.0.1:5000/suggest", json={"query": query})
            response.raise_for_status()
            results = response.json().get("suggestions", [])
        except Exception as e:
            self.results_list.addItem(QListWidgetItem(f"Error fetching videos: {e}"))
            return

        for title, desc, thumb_url, url in results:
            item_widget = QWidget()
            layout = QVBoxLayout()

            # Thumbnail
            thumb_label = QLabel()
            try:
                img_data = requests.get(thumb_url).content
                pixmap = QPixmap()
                pixmap.loadFromData(img_data)
                thumb_label.setPixmap(pixmap.scaledToHeight(100, Qt.SmoothTransformation))
            except:
                thumb_label.setText("[Thumbnail not available]")

            # Title, Description, URL
            title_label = QLabel(f"<b>{title}</b>")
            title_label.setWordWrap(True)

            desc_label = QLabel(desc)
            desc_label.setWordWrap(True)

            url_label = QLabel(f'<a href="{url}">{url}</a>')
            url_label.setOpenExternalLinks(True)

            layout.addWidget(thumb_label)
            layout.addWidget(title_label)
            layout.addWidget(desc_label)
            layout.addWidget(url_label)

            item_widget.setLayout(layout)
            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())

            self.results_list.addItem(list_item)
            self.results_list.setItemWidget(list_item, item_widget)

    def format_stats(self):
        stats = self.user_data.get("stats", {})
        total = stats.get("total_searches", 0)
        last = self.user_data.get("last_active", "N/A")
        most = self.user_data.get("most_searched", "N/A")
        return f"Total Searches: {total} | Last Active: {last} | Most Searched: {most}"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = HistomendDashboard()
    dashboard.show()
    sys.exit(app.exec_())

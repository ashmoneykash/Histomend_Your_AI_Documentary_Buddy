import sys
import json
import requests
from io import BytesIO
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QListWidget, QListWidgetItem, 
                             QFrame, QScrollArea, QGridLayout, QSplitter, QSpacerItem,
                             QSizePolicy)
from PyQt5.QtGui import QFont, QPixmap, QColor, QPalette, QFontDatabase, QIcon
from PyQt5.QtCore import Qt, QFile, QTextStream, QSize
from user_profile import load_user_data, update_search_history


class CustomQFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setObjectName("customFrame")


class HistomendDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Histomend - Fantasy Dashboard")
        self.setGeometry(100, 50, 1200, 800)  # Increased window size

        # Load fonts
        QFontDatabase.addApplicationFont("frontend/fonts/Roboto-Regular.ttf")
        QFontDatabase.addApplicationFont("frontend/fonts/Roboto-Bold.ttf")

        self.dark_mode = True  # Start in dark mode by default based on reference image
        self.user_data = load_user_data()
        
        # Define theme colors based on reference image
        self.dark_colors = {
            "bg_primary": "#121212",
            "bg_secondary": "#1E1E1E",
            "accent": "#2ECC71",  # Green accent color from image
            "text_primary": "#FFFFFF",
            "text_secondary": "#AAAAAA",
            "border": "#333333",
            "hover": "#2ECC71",
            "button_bg": "#2A2A2A"
        }
        
        self.light_colors = {
            "bg_primary": "#F5F5F5",
            "bg_secondary": "#FFFFFF",
            "accent": "#27AE60",
            "text_primary": "#333333",
            "text_secondary": "#666666",
            "border": "#DDDDDD",
            "hover": "#27AE60",
            "button_bg": "#EEEEEE"
        }

        self.init_ui()
        self.apply_theme()  # Apply initial theme

    def apply_theme(self):
        colors = self.dark_colors if self.dark_mode else self.light_colors
        
        # Create stylesheet dynamically with colors
        stylesheet = f"""
        QWidget {{
            background-color: {colors['bg_primary']};
            color: {colors['text_primary']};
            font-family: 'Roboto';
        }}
        
        QFrame#customFrame {{
            background-color: {colors['bg_secondary']};
            border-radius: 10px;
            border: 1px solid {colors['border']};
        }}
        
        QLabel {{
            color: {colors['text_primary']};
        }}
        
        QLabel[objectName="statsLabel"] {{
            color: {colors['text_secondary']};
            padding: 5px;
        }}
        
        QLabel[objectName="usernameLabel"] {{
            font-size: 18px;
            font-weight: bold;
        }}
        
        QPushButton {{
            background-color: {colors['button_bg']};
            border-radius: 5px;
            padding: 8px 15px;
            font-weight: bold;
            border: none;
        }}
        
        QPushButton:hover {{
            background-color: {colors['hover']};
            color: white;
        }}
        
        QPushButton#searchBtn {{
            background-color: {colors['accent']};
            color: white;
        }}
        
        QLineEdit {{
            background-color: {colors['bg_secondary']};
            border: 1px solid {colors['border']};
            border-radius: 5px;
            padding: 8px;
            color: {colors['text_primary']};
        }}
        
        QListWidget {{
            background-color: {colors['bg_secondary']};
            border-radius: 10px;
            padding: 5px;
            outline: none;
            border: 1px solid {colors['border']};
        }}
        
        QListWidget::item {{
            border-bottom: 1px solid {colors['border']};
            padding: 5px;
        }}
        
        QListWidget::item:selected {{
            background-color: {colors['accent']};
            color: white;
        }}
        """
        
        self.setStyleSheet(stylesheet)
        self.repaint()  # Force repaint to apply style

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        self.theme_button.setText("☀️ Light Mode" if self.dark_mode else "🌙 Dark Mode")

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header section with logo and user info
        header_frame = CustomQFrame()
        header_layout = QHBoxLayout(header_frame)

        logo_label = QLabel("🧙‍♂️ HISTOMEND")
        logo_label.setFont(QFont("Roboto", 16, QFont.Bold))
        
        self.username_label = QLabel(f"Welcome, {self.user_data['username']}")
        self.username_label.setObjectName("usernameLabel")
        
        self.theme_button = QPushButton("☀️ Light Mode" if self.dark_mode else "🌙 Dark Mode")
        self.theme_button.setFixedWidth(150)
        self.theme_button.clicked.connect(self.toggle_theme)
        
        header_layout.addWidget(logo_label)
        header_layout.addStretch()
        header_layout.addWidget(self.username_label)
        header_layout.addWidget(self.theme_button)

        # Search section
        search_frame = CustomQFrame()
        search_layout = QHBoxLayout(search_frame)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for educational videos...")
        self.search_input.setMinimumHeight(40)
        
        self.search_button = QPushButton("Search")
        self.search_button.setObjectName("searchBtn")
        self.search_button.setMinimumHeight(40)
        self.search_button.setFixedWidth(120)
        self.search_button.clicked.connect(self.perform_search)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        # Main content area with results
        content_frame = CustomQFrame()
        content_layout = QVBoxLayout(content_frame)
        
        results_label = QLabel("Search Results")
        results_label.setFont(QFont("Roboto", 14, QFont.Bold))
        
        self.results_list = QListWidget()
        self.results_list.setSpacing(10)
        
        content_layout.addWidget(results_label)
        content_layout.addWidget(self.results_list)

        # Footer with stats
        footer_frame = CustomQFrame()
        footer_layout = QHBoxLayout(footer_frame)
        
        self.stats_label = QLabel(self.format_stats())
        self.stats_label.setObjectName("statsLabel")
        
        footer_layout.addWidget(self.stats_label)
        footer_layout.addStretch()

        # Add all sections to main layout
        main_layout.addWidget(header_frame)
        main_layout.addWidget(search_frame)
        main_layout.addWidget(content_frame, 1)  # Give content area more space
        main_layout.addWidget(footer_frame)
        
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
            error_item = QListWidgetItem()
            error_widget = QLabel(f"Error fetching videos: {e}")
            error_item.setSizeHint(error_widget.sizeHint())
            self.results_list.addItem(error_item)
            self.results_list.setItemWidget(error_item, error_widget)
            return

        if not results:
            no_results = QListWidgetItem()
            no_results_widget = QLabel("No results found. Try different keywords.")
            no_results.setSizeHint(no_results_widget.sizeHint())
            self.results_list.addItem(no_results)
            self.results_list.setItemWidget(no_results, no_results_widget)
            return

        for title, desc, thumb_url, url in results:
            # Create a nice looking result card
            item_widget = QWidget()
            layout = QHBoxLayout()
            
            # Left side - thumbnail
            thumb_frame = QFrame()
            thumb_layout = QVBoxLayout(thumb_frame)
            thumb_label = QLabel()
            thumb_label.setFixedSize(150, 100)
            thumb_label.setScaledContents(True)
            thumb_label.setStyleSheet("background-color: #2A2A2A; border-radius: 5px;")
            
            try:
                img_data = requests.get(thumb_url).content
                pixmap = QPixmap()
                pixmap.loadFromData(img_data)
                thumb_label.setPixmap(pixmap.scaledToHeight(100, Qt.SmoothTransformation))
            except:
                thumb_label.setText("[Thumbnail]")
                thumb_label.setAlignment(Qt.AlignCenter)
            
            thumb_layout.addWidget(thumb_label)
            
            # Right side - text content
            content_frame = QFrame()
            content_layout = QVBoxLayout(content_frame)
            
            title_label = QLabel(f"<b>{title}</b>")
            title_label.setFont(QFont("Roboto", 12, QFont.Bold))
            title_label.setWordWrap(True)
            
            desc_label = QLabel(desc)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("color: #AAAAAA;")
            
            url_label = QLabel(f'<a href="{url}" style="color: #2ECC71;">{url}</a>')
            url_label.setOpenExternalLinks(True)
            
            content_layout.addWidget(title_label)
            content_layout.addWidget(desc_label)
            content_layout.addWidget(url_label)
            content_layout.setContentsMargins(10, 5, 5, 5)
            
            # Add to main layout
            layout.addWidget(thumb_frame)
            layout.addWidget(content_frame)
            layout.setStretch(0, 1)  # Thumbnail takes less space
            layout.setStretch(1, 3)  # Content takes more space
            
            item_widget.setLayout(layout)
            list_item = QListWidgetItem()
            list_item.setSizeHint(QSize(self.results_list.width(), 120))
            
            self.results_list.addItem(list_item)
            self.results_list.setItemWidget(list_item, item_widget)

    def format_stats(self):
        stats = self.user_data.get("stats", {})
        total = stats.get("total_searches", 0)
        last = self.user_data.get("last_active", "N/A")
        most = self.user_data.get("most_searched", "N/A")
        return f"📊 Stats | Total Searches: {total} | Last Active: {last} | Most Searched: {most}"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dashboard = HistomendDashboard()
    dashboard.show()
    sys.exit(app.exec_())
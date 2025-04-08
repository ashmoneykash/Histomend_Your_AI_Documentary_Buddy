# gui.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QTextBrowser
import requests

class DocumentaryFinder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Histomend")
        self.setGeometry(100, 100, 500, 400)

        self.layout = QVBoxLayout()
        self.label = QLabel("Enter a Historical Topic:")
        self.input = QLineEdit()
        self.button = QPushButton("Find Documentaries")
        self.output = QTextBrowser()

        self.button.clicked.connect(self.get_recommendations)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.output)

        self.setLayout(self.layout)

    def get_recommendations(self):
        query = self.input.text()
        res = requests.post('http://127.0.0.1:5000/suggest', json={'query': query})
        data = res.json()
        self.output.clear()
        for item in data:
            self.output.append(f"<b>{item['title']}</b><br><img src='{item['thumbnail']}'><br><a href='https://youtube.com/watch?v={item['videoId']}'>Watch</a><br><br>")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = DocumentaryFinder()
    win.show()
    sys.exit(app.exec_())

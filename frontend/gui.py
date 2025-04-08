import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget

class HistomendApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Histomend - Your AI Documentary Buddy")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel("Enter a historical topic:")
        self.input = QLineEdit()
        self.button = QPushButton("Find Documentaries")
        self.result_list = QListWidget()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.result_list)

        self.setLayout(self.layout)

        self.button.clicked.connect(self.get_suggestions)

    def get_suggestions(self):
        topic = self.input.text()
        response = requests.post("http://127.0.0.1:5000/suggest", json={"query": topic})
        if response.status_code == 200:
            data = response.json()
            self.result_list.clear()
            for doc in data["suggestions"]:
                self.result_list.addItem(doc)
        else:
            self.result_list.clear()
            self.result_list.addItem("Error retrieving suggestions.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HistomendApp()
    window.show()
    sys.exit(app.exec_())

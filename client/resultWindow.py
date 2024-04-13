import sys

from PyQt5.QtWidgets import QLabel, QApplication
from BaseWindow import BaseWindow  # Assuming BaseWindow is your custom base class


class ResultWindow(BaseWindow):  # Corrected class name
    def __init__(self, results, url):
        super().__init__("results", "pictures\\results.png")

        self.sqlres_label = QLabel(self)
        self.sqlres_label.setText(str(results.get("test1", "")))  # Handle potential missing key
        self.sqlres_label.setGeometry(343, 341, 30, 40)
        self.sqlres_label.setStyleSheet("""
                    color: white;
                    background-color: transparent;
                    font-size: 30px;
                    font-family: 'Poppins';
                    font-weight: 0;
                """)

        self.xssres_label = QLabel(self)
        self.xssres_label.setText(str(results.get("test2", "")))  # Handle potential missing key
        self.xssres_label.setGeometry(333, 560, 30, 40)
        self.xssres_label.setStyleSheet("""
                            color: white;
                            background-color: transparent;
                            font-size: 30px;
                            font-family: 'Poppins';
                            font-weight: 0;
                        """)

        self.url_label = QLabel(self)
        self.url_label.setText(self.process_url(url))
        self.url_label.setGeometry(415, 40, 1000, 100)
        self.url_label.setStyleSheet("""
                                    color: white;
                                    background-color: transparent;
                                    font-size: 30px;
                                    font-family: 'Poppins';
                                    font-weight: 0;
                                """)

    def process_url(self, url):
        if len(url) > 45:
            new_url = ""
            for i, char in enumerate(url):
                new_url += char
                if (i + 1) % 40 == 0:  # Adding 1 to ensure it doesn't insert at index 0
                    new_url += "\n"
            return new_url
        return url


def show_results(test_results, url):
    app = QApplication(sys.argv)
    window = ResultWindow(test_results, url)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Your main window code here (if applicable)

    results = {'test1': 2, 'test2': 2}
    url = "http://testphp.vulnweb.com/artists.php?artist=1"
    show_results(results, url)

from PyQt5.QtWidgets import QLabel
from BaseWindow import BaseWindow


class ResultlWindow(BaseWindow):
    def __init__(self, results, url):
        super().__init__("results", "pictures\\results.png")

        self.sqlres_label = QLabel(self)
        self.sqlres_label.setText(str(results.get("test1")))
        self.sqlres_label.setGeometry(343, 341, 30, 40)
        self.sqlres_label.setStyleSheet("""
                    color: white;
                    background-color: transparent;
                    font-size: 30px;
                    font-family: 'Poppins';
                    font-weight: 0;
                """)

        self.xssres_label = QLabel(self)
        self.xssres_label.setText(str(results.get("test2")))
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
                if (i + 1) % 45 == 0:  # Adding 1 to ensure it doesn't insert at index 0
                    new_url += "\n"
            return new_url
        return url


def show_results(test_results, url):
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = ResultlWindow(test_results, url)
    window.show()
    sys.exit(app.exec_())

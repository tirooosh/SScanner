import sys

from PyQt5.QtWidgets import QLabel, QApplication
from BaseWindow import BaseWindow


class ResultWindow(BaseWindow):
    def __init__(self, sqltest, xsstest, url):
        super().__init__("results", "pictures\\results.png")

        self.sqlres_label = QLabel(self)
        self.sqlres_label.setText(str(sqltest))
        self.sqlres_label.setGeometry(343, 341, 30, 40)
        self.sqlres_label.setStyleSheet("""
                    color: white;
                    background-color: transparent;
                    font-size: 30px;
                    font-family: 'Poppins';
                    font-weight: 0;
                """)

        self.xssres_label = QLabel(self)
        self.xssres_label.setText(str(xsstest))  # Handle potential missing key
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

        self.vulnerable_label_sql = QLabel(self)
        self.vulnerable_label_sql.setGeometry(762, 310, 1000, 100)
        self.vulnerable_label_sql.setStyleSheet("""
                                            color: white;
                                            background-color: transparent;
                                            font-size: 30px;
                                            font-family: 'Poppins';
                                            font-weight: 0;
                                        """)

        self.vulnerable_label_xss = QLabel(self)
        self.vulnerable_label_xss.setGeometry(750, 531, 1000, 100)
        self.vulnerable_label_xss.setStyleSheet("""
                                                    color: white;
                                                    background-color: transparent;
                                                    font-size: 30px;
                                                    font-family: 'Poppins';
                                                    font-weight: 0;
                                                """)
        self.process_results(sqltest, xsstest)

    def process_url(self, url):
        if len(url) > 45:
            new_url = ""
            for i, char in enumerate(url):
                new_url += char
                if (i + 1) % 40 == 0:  # Adding 1 to ensure it doesn't insert at index 0
                    new_url += "\n"
            return new_url
        return url

    def process_results(self, sqltest, xsstest):
        if int(sqltest) > 0:
            self.vulnerable_label_sql.setText("vulnerable")
        else:
            self.vulnerable_label_sql.setText("not vulnerable")

        if int(xsstest) > 0:
            self.vulnerable_label_xss.setText("vulnerable")
        else:
            self.vulnerable_label_xss.setText("not vulnerable")


def show_results(sqltest, xsstest, url):
    app = QApplication(sys.argv)
    window = ResultWindow(sqltest, xsstest, url)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Your main window code here (if applicable)
    url = "http://testphp.vulnweb.com/artists.php?artist=1"
    show_results(1,1, url)

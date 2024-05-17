import sys
import webbrowser

from PyQt5.QtWidgets import QLabel, QApplication
from BaseWindow import BaseWindow


class ResultWindow(BaseWindow):
    def __init__(self, sqltest, xsstest, url):
        super().__init__("results", "pictures\\results.png")

        self.setupLabels(self.process_url(url), (160, 40), (1000, 100))

        self.setupLabels(self.process_grade(sqltest[0]), (490, 265), (100, 100))
        self.setupLabels(self.process_grade(sqltest[1]), (440, 387), (100, 100))
        self.setupLabels(self.process_grade(sqltest[2]), (180, 512), (100, 100))
        self.setupLabels(self.process_grade(sqltest[3]), (155, 635), (100, 100))

        self.setupLabels(self.process_grade(xsstest[0]), (1125, 265), (100, 100))
        self.setupLabels(self.process_grade(xsstest[1]), (1075, 390), (100, 100))

        self.setup_buttons("sql t1", (30, 290), (45, 40), lambda: webbrowser.open("https://www.w3schools.com/sql/sql_injection.asp", new=0, autoraise=True))
        self.setup_buttons("sql t2", (30, 412), (50, 40), lambda: webbrowser.open("https://www.w3schools.com/sql/sql_injection.asp", new=0, autoraise=True))
        self.setup_buttons("sql t3", (30, 540), (45, 40), lambda: webbrowser.open("https://subscription.packtpub.com/book/web-development/9781838643577/2/ch02lvl1sec16/sql-injection-in-urls-and-ways-to-avoid-them", new=0, autoraise=True))
        self.setup_buttons("sql t4", (30, 660), (45, 40), lambda: webbrowser.open("https://security.stackexchange.com/questions/173459/sql-injection-how-to-find-urls-to-attack-to", new=0, autoraise=True))

        self.setup_buttons("xss t1", (663, 290), (45, 40), lambda: webbrowser.open("https://www.synopsys.com/glossary/what-is-cross-site-scripting.html", new=0, autoraise=True))
        self.setup_buttons("xss t2", (663, 412), (50, 40), lambda: webbrowser.open("https://www.synopsys.com/glossary/what-is-cross-site-scripting.html", new=0, autoraise=True))

        self.button.setStyleSheet("background-color: #172633;font-size: 18px;font-weight: 500;")

    def process_grade(self, bool):
        if bool:
            return "failed"
        else:
            return "passed"

    def process_url(self, url):
        if len(url) > 65:
            new_url = ""
            for i, char in enumerate(url):
                new_url += char
                if (i + 1) % 60 == 0:  # Adding 1 to ensure it doesn't insert at index 0
                    new_url += "\n"
            return new_url
        return url

    def setupLabels(self, text, location, size):
        lbl = QLabel(self)
        lbl.setText(text)
        lbl.setGeometry(location[0], location[1], size[0], size[1])
        lbl.setStyleSheet("""
                                    color: white;
                                    background-color: transparent;
                                    font-size: 30px;
                                    font-family: 'Poppins';
                                    font-weight: 0;
                                """)


def show_results(sqltest, xsstest, url):
    app = QApplication(sys.argv)
    window = ResultWindow(sqltest, xsstest, url)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    # Your main window code here (if applicable)
    url = "http://testphp.vulnweb.com/artists.php?artist=1"
    show_results([False, False, True, True], [True, True], url)

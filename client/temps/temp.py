import sys
from PyQt5.QtWidgets import QApplication, QWidget, QProgressBar, QVBoxLayout
from PyQt5.QtCore import QTimer
import threading

class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.testInProgress = True
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Penetration Testing Progress')

        self.layout = QVBoxLayout(self)
        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(180)  # 180 seconds (3 minutes)
        self.layout.addWidget(self.progressBar)
        self.setLayout(self.layout)

        # Timer update
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgressBar)
        self.timer.start(1000)  # 1000 milliseconds (1 second)

    def updateProgressBar(self):
        if self.progressBar.value() < 180 and self.testInProgress:
            self.progressBar.setValue(self.progressBar.value() + 1)
        else:
            self.timer.stop()  # Stop timer if maximum is reached or test is done
            self.close()

    def runPentest(self):
        while True:
            if input("should i stop?") == "yes":
                self.testInProgress = False

def main():
    app = QApplication(sys.argv)
    testWindow = TestWindow()
    testWindow.show()

    # Start the pentest in a separate thread
    threading.Thread(target=testWindow.runPentest).start()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

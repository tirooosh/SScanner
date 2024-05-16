from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap, QPainter, QTransform
from PyQt5.QtCore import QTimer, Qt
from BaseWindow import BaseWindow

class LoadingScreens(BaseWindow):
    def __init__(self):
        super().__init__("Loading Screen", "pictures\\loadingscreen.png")
        self.num_legs = 0  # Number of legs displayed (each pair counts as two)
        self.leg_spacing = 50  # Horizontal space between legs
        self.x_pos = 400  # Starting x position for the first leg
        self.x_increment = 30  # Increment for x position of the second leg in each pair
        self.max_legs = 19  # Maximum number of legs
        self.adding_second_leg = False  # Track if adding second leg in pair

        # Calculate appropriate pixmap dimensions
        self.pixmap = QPixmap(self.width(), self.height())
        self.pixmap.fill(Qt.transparent)  # Initialize pixmap as transparent

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('Loading Screen')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.add_legs)
        self.timer.start(500)  # Start with 500 milliseconds for the first leg

    def add_legs(self):
        if self.num_legs < self.max_legs:
            base_x_position = self.x_pos + (self.num_legs // 2) * self.leg_spacing
            y_position = 635 if not self.adding_second_leg else 652
            x_position = base_x_position if not self.adding_second_leg else base_x_position + self.x_increment
            scale = 0.4

            self.draw_leg(x_position, y_position, scale)
            self.num_legs += 1
            self.update()  # Redraw window

            if not self.adding_second_leg:
                self.adding_second_leg = True
                self.timer.start(500)  # Same delay for the second leg
            else:
                self.adding_second_leg = False
                self.timer.start(1000)  # Twice the delay before the next set
        else:
            self.reset_animation()

    def reset_animation(self):
        self.pixmap.fill(Qt.transparent)  # Clear the pixmap
        self.num_legs = 0  # Reset the leg counter
        self.adding_second_leg = False  # Reset leg pair state
        self.timer.start(500)  # Restart the timer

    def draw_leg(self, x, y, scale):
        leg_pixmap = QPixmap("pictures\\etc\\duck_legs.png")
        if leg_pixmap.isNull():
            print("Failed to load leg image")
            return
        # Scale down the pixmap
        transform = QTransform().scale(scale, scale)
        scaled_pixmap = leg_pixmap.transformed(transform, Qt.SmoothTransformation)
        painter = QPainter(self.pixmap)
        painter.drawPixmap(x, y, scaled_pixmap)
        painter.end()

    def paintEvent(self, event):
        super().paintEvent(event)  # Ensure background is painted
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)  # Draw the legs pixmap

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = LoadingScreens()
    window.show()
    sys.exit(app.exec_())

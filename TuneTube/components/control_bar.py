from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QSlider
)

from PyQt5.QtCore import (
    Qt,
    QSize,
    QTimer,
    pyqtSignal
)

from PyQt5.QtGui import QIcon


# ==========================================================
# CONTROL BAR
# ==========================================================

class ControlBar(QWidget):

    play_pause_clicked = pyqtSignal()
    volume_changed = pyqtSignal(int)

    def __init__(self):

        super().__init__()

        layout = QHBoxLayout()

# ----------------------------------------------------------
# PLAY / PAUSE BUTTON
# ----------------------------------------------------------

        self.play_button = QPushButton()

        self.play_button.setIcon(QIcon("images/play.png"))
        self.play_button.setIconSize(QSize(64, 64))
        self.play_button.setFixedSize(80, 80)

        self.play_button.clicked.connect(
            self.play_pause_clicked.emit
        )

        layout.addWidget(self.play_button)

# ----------------------------------------------------------
# VOLUME
# ----------------------------------------------------------

        volume_layout = QVBoxLayout()

        self.volume_slider = QSlider(Qt.Vertical)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setFixedSize(50, 120)
        self.volume_slider.hide()

        # Forward slider value straight out as our signal
        self.volume_slider.valueChanged.connect(
            self.volume_changed
        )

        self.volume_button = QPushButton()
        self.volume_button.setIcon(QIcon("images/volume.png"))
        self.volume_button.setIconSize(QSize(40, 40))
        self.volume_button.setFixedSize(50, 50)
        self.volume_button.clicked.connect(
            self.toggle_volume_slider
        )

        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.volume_slider.hide)

        volume_layout.addWidget(self.volume_slider)
        volume_layout.addWidget(self.volume_button)

        layout.addLayout(volume_layout)

        self.setLayout(layout)

# ==========================================================
# TOGGLE VOLUME SLIDER
# ==========================================================

    def toggle_volume_slider(self):

        if self.volume_slider.isVisible():
            self.volume_slider.hide()
        else:
            self.volume_slider.show()
            self.hide_timer.start(2000)

# ==========================================================
# ICON HELPERS  (called by main_window)
# ==========================================================

    def set_play_icon(self):
        self.play_button.setIcon(QIcon("images/play.png"))

    def set_pause_icon(self):
        self.play_button.setIcon(QIcon("images/pause.png"))
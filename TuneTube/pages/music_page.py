import os

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget
)


# ==========================================================
# MUSIC PAGE
# ==========================================================

class MusicPage(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel("🎵 Music Player"))

        self.song_list = QListWidget()

        layout.addWidget(self.song_list)

        self.setLayout(layout)

# ==========================================================
# LOAD SONGS
# ==========================================================

    def load_songs(self, download_dir):

        self.song_list.clear()

        songs = [
            f for f in os.listdir(download_dir)
            if f.endswith(".mp3")
        ]

        self.song_list.addItems(songs)
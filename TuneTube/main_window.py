import os
import pygame

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QStackedWidget
)

from pages.music_page import MusicPage
from pages.download_page import DownloadPage
from components.control_bar import ControlBar


# ==========================================================
# MAIN WINDOW
# ==========================================================

class MusicPlayerApp(QWidget):

    def __init__(self):

        super().__init__()

        pygame.mixer.init()

        self.current_song = None
        self.is_paused = False

        self.base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        self.download_dir = os.path.join(
            self.base_dir,
            "downloads"
        )

        os.makedirs(
            self.download_dir,
            exist_ok=True
        )

        self.initUI()

# ==========================================================
# UI
# ==========================================================

    def initUI(self):

        main_layout = QVBoxLayout()

# ----------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------

        content_layout = QHBoxLayout()

        self.sidebar = QListWidget()

        self.sidebar.addItem("🎵 Music Player")
        self.sidebar.addItem("📥 YouTube Downloader")

        self.sidebar.setFixedWidth(180)

# ----------------------------------------------------------
# PAGES
# ----------------------------------------------------------

        self.pages = QStackedWidget()

        self.music_page = MusicPage()
        self.music_page.load_songs(self.download_dir)
        self.music_page.song_list.itemDoubleClicked.connect(
            self.play_song
        )

        self.download_page = DownloadPage(self.download_dir)
        self.download_page.download_complete.connect(
            self.on_download_complete
        )

        self.pages.addWidget(self.music_page)
        self.pages.addWidget(self.download_page)

        self.sidebar.currentRowChanged.connect(
            self.pages.setCurrentIndex
        )

        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.pages)

# ----------------------------------------------------------
# CONTROL BAR
# ----------------------------------------------------------

        self.control_bar = ControlBar()

        self.control_bar.play_pause_clicked.connect(
            self.toggle_play_pause
        )

        self.control_bar.volume_changed.connect(
            self.set_volume
        )

# ----------------------------------------------------------
# ASSEMBLE
# ----------------------------------------------------------

        main_layout.addLayout(content_layout)
        main_layout.addWidget(self.control_bar)

        self.setLayout(main_layout)

        self.setWindowTitle("TuneTube")
        self.setGeometry(100, 100, 1400, 800)

# ==========================================================
# PLAY SONG
# ==========================================================

    def play_song(self):

        selected_song = (
            self.music_page.song_list.currentItem()
        )

        if not selected_song:
            return

        song_path = os.path.join(
            self.download_dir,
            selected_song.text()
        )

        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()

        self.current_song = song_path
        self.is_paused = False

        self.control_bar.set_pause_icon()

# ==========================================================
# PLAY / PAUSE
# ==========================================================

    def toggle_play_pause(self):

        if not self.current_song:

            if self.music_page.song_list.count() > 0:

                self.music_page.song_list.setCurrentRow(0)
                self.play_song()

            return

        if self.is_paused:

            pygame.mixer.music.unpause()

            self.control_bar.set_pause_icon()

            self.is_paused = False

        else:

            pygame.mixer.music.pause()

            self.control_bar.set_play_icon()

            self.is_paused = True

# ==========================================================
# VOLUME
# ==========================================================

    def set_volume(self, value):

        pygame.mixer.music.set_volume(value / 100)

# ==========================================================
# DOWNLOAD COMPLETE CALLBACK
# ==========================================================

    def on_download_complete(self):

        self.music_page.load_songs(self.download_dir)
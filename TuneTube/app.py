import sys
import os
import pygame
import ssl

from downloader import download_song as yt_download

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QLabel,
    QStackedWidget,
    QPushButton,
    QSlider,
    QLineEdit,
    QProgressBar
)

from PyQt5.QtCore import (
    QSize,
    Qt,
    QTimer
)

from PyQt5.QtGui import QIcon


# ==========================================================
# FIX SSL
# ==========================================================

ssl._create_default_https_context = (
    ssl._create_unverified_context
)


# ==========================================================
# MAIN APP
# ==========================================================

class MusicPlayerApp(QWidget):

    def __init__(self):

        super().__init__()

        pygame.mixer.init()

        self.current_song = None
        self.is_paused = False

        # Base folder
        self.base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )

        # Downloads folder
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

# ==========================================================
# SIDEBAR + PAGES
# ==========================================================

        content_layout = QHBoxLayout()

        self.sidebar = QListWidget()

        self.sidebar.addItem(
            "🎵 Music Player"
        )

        self.sidebar.addItem(
            "📥 YouTube Downloader"
        )

        self.sidebar.setFixedWidth(180)

        self.pages = QStackedWidget()

# ==========================================================
# MUSIC PAGE
# ==========================================================

        self.music_page = QWidget()

        self.music_layout = QVBoxLayout()

        self.music_layout.addWidget(
            QLabel("🎵 Music Player")
        )

        self.song_list = QListWidget()

        self.music_layout.addWidget(
            self.song_list
        )

        self.music_page.setLayout(
            self.music_layout
        )

# ==========================================================
# DOWNLOAD PAGE
# ==========================================================

        self.download_page = QWidget()

        download_layout = QVBoxLayout()

        download_layout.addWidget(
            QLabel("📥 YouTube Downloader")
        )

# URL INPUT

        self.url_input = QLineEdit()

        self.url_input.setPlaceholderText(
            "Paste YouTube URL..."
        )

        download_layout.addWidget(
            self.url_input
        )

# DOWNLOAD BUTTON

        self.download_button = QPushButton(
            "Download"
        )

        self.download_button.clicked.connect(
            self.download_song
        )

        download_layout.addWidget(
            self.download_button
        )

# PROGRESS BAR

        self.progress_bar = QProgressBar()

        self.progress_bar.setValue(0)

        download_layout.addWidget(
            self.progress_bar
        )

# STATUS LABEL

        self.download_status = QLabel("")

        download_layout.addWidget(
            self.download_status
        )

        self.download_page.setLayout(
            download_layout
        )

# ==========================================================
# ADD PAGES
# ==========================================================

        self.pages.addWidget(
            self.music_page
        )

        self.pages.addWidget(
            self.download_page
        )

        self.sidebar.currentRowChanged.connect(
            self.pages.setCurrentIndex
        )

        content_layout.addWidget(
            self.sidebar
        )

        content_layout.addWidget(
            self.pages
        )

# ==========================================================
# CONTROL BAR
# ==========================================================

        self.control_bar = QHBoxLayout()

# PLAY BUTTON

        self.play_button = QPushButton()

        self.play_button.setIcon(
            QIcon("images/play.png")
        )

        self.play_button.setIconSize(
            QSize(64, 64)
        )

        self.play_button.setFixedSize(
            80,
            80
        )

        self.play_button.clicked.connect(
            self.toggle_play_pause
        )

        self.control_bar.addWidget(
            self.play_button
        )

# ==========================================================
# VOLUME
# ==========================================================

        self.volume_layout = QVBoxLayout()

# VOLUME SLIDER

        self.volume_slider = QSlider(
            Qt.Vertical
        )

        self.volume_slider.setRange(
            0,
            100
        )

        self.volume_slider.setValue(50)

        self.volume_slider.setFixedSize(
            50,
            120
        )

        self.volume_slider.hide()

        self.volume_slider.valueChanged.connect(
            self.set_volume
        )

# VOLUME BUTTON

        self.volume_button = QPushButton()

        self.volume_button.setIcon(
            QIcon("images/volume.png")
        )

        self.volume_button.setIconSize(
            QSize(40, 40)
        )

        self.volume_button.setFixedSize(
            50,
            50
        )

        self.volume_button.clicked.connect(
            self.toggle_volume_slider
        )

# TIMER

        self.hide_timer = QTimer()

        self.hide_timer.setSingleShot(True)

        self.hide_timer.timeout.connect(
            self.volume_slider.hide
        )

# ADD TO VOLUME LAYOUT

        self.volume_layout.addWidget(
            self.volume_slider
        )

        self.volume_layout.addWidget(
            self.volume_button
        )

        self.control_bar.addLayout(
            self.volume_layout
        )

# ==========================================================
# FINAL LAYOUT
# ==========================================================

        main_layout.addLayout(
            content_layout
        )

        main_layout.addLayout(
            self.control_bar
        )

        self.setLayout(main_layout)

# ==========================================================
# LOAD SONGS
# ==========================================================

        self.load_songs()

        self.song_list.itemDoubleClicked.connect(
            self.play_song
        )

# WINDOW SETTINGS

        self.setWindowTitle(
            "TuneTube"
        )

        self.setGeometry(
            100,
            100,
            1400,
            800
        )

# ==========================================================
# LOAD SONGS
# ==========================================================

    def load_songs(self):

        self.song_list.clear()

        songs = [

            f for f in os.listdir(
                self.download_dir
            )

            if f.endswith(".mp3")
        ]

        self.song_list.addItems(
            songs
        )

# ==========================================================
# PLAY SONG
# ==========================================================

    def play_song(self):

        selected_song = (
            self.song_list.currentItem()
        )

        if not selected_song:
            return

        song_path = os.path.join(
            self.download_dir,
            selected_song.text()
        )

        pygame.mixer.music.load(
            song_path
        )

        pygame.mixer.music.play()

        self.current_song = song_path

        self.is_paused = False

        self.play_button.setIcon(
            QIcon("images/pause.png")
        )

# ==========================================================
# PLAY / PAUSE
# ==========================================================

    def toggle_play_pause(self):

        if not self.current_song:

            if self.song_list.count() > 0:

                self.song_list.setCurrentRow(0)

                self.play_song()

            return

        if self.is_paused:

            pygame.mixer.music.unpause()

            self.play_button.setIcon(
                QIcon("images/pause.png")
            )

            self.is_paused = False

        else:

            pygame.mixer.music.pause()

            self.play_button.setIcon(
                QIcon("images/play.png")
            )

            self.is_paused = True

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
# SET VOLUME
# ==========================================================

    def set_volume(self, value):

        pygame.mixer.music.set_volume(
            value / 100
        )

# ==========================================================
# UPDATE PROGRESS BAR
# ==========================================================

    def update_progress(self, d):

        if d['status'] == 'downloading':

            percent = d.get(
                '_percent_str',
                '0%'
            )

            percent = percent.replace(
                '%',
                ''
            ).strip()

            try:

                self.progress_bar.setValue(
                    int(float(percent))
                )

            except:
                pass

        elif d['status'] == 'finished':

            self.progress_bar.setValue(100)

# ==========================================================
# DOWNLOAD SONG
# ==========================================================

    def download_song(self):

        url = self.url_input.text().strip()

        if not url:

            self.download_status.setText(
                "Enter a valid URL"
            )

            return

        self.download_status.setText(
            "Downloading..."
        )

        self.progress_bar.setValue(0)

        success = yt_download(
            url,
            self.update_progress
        )

        if success:

            self.download_status.setText(
                "Download Complete!"
            )

            self.load_songs()

        else:

            self.download_status.setText(
                "Download Failed!"
            )

# ==========================================================
# RUN APP
# ==========================================================

if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MusicPlayerApp()

    window.show()

    sys.exit(app.exec_())
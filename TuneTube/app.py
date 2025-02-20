import sys
import os
import pygame
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QStackedWidget, QPushButton
from PyQt5.QtCore import QSize, QFile, QTextStream
from PyQt5.QtGui import QIcon


class MusicPlayerApp(QWidget):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()  # Initialize pygame mixer
        self.current_song = None  # Keep track of the current song
        self.initUI()

#----------------------------------------------------------------------------------------------------------#

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()

        # Sidebar and pages layout
        content_layout = QHBoxLayout()
        self.sidebar = QListWidget()
        self.sidebar.addItem("🎵 Music Player")
        self.sidebar.addItem("📥 YouTube Downloader")
        self.sidebar.setFixedWidth(150)

        # Stack to hold different pages
        self.pages = QStackedWidget()

        # Music Player Page
        self.music_page = QWidget()
        self.music_layout = QVBoxLayout()
        self.song_list = QListWidget()
        self.music_layout.addWidget(QLabel("🎵 Music Player Interface"))
        self.music_layout.addWidget(self.song_list)
        self.music_page.setLayout(self.music_layout)

        # YouTube Downloader Page
        self.download_page = QWidget()
        download_layout = QVBoxLayout()
        download_layout.addWidget(QLabel("📥 YouTube Downloader Interface"))
        self.download_page.setLayout(download_layout)

        # Add pages to the stack
        self.pages.addWidget(self.music_page)
        self.pages.addWidget(self.download_page)

        # Sidebar navigation functionality
        self.sidebar.currentRowChanged.connect(self.pages.setCurrentIndex)

        # Add sidebar and pages to the content layout
        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.pages)

        # Persistent Bottom Control Bar
        self.control_bar = QHBoxLayout()

        self.play_button = QPushButton()
        self.play_button.setObjectName("playButton")
        self.play_button.setIcon(QIcon("images/play.png"))
        self.play_button.setIconSize(QSize(64, 64))
        self.play_button.setFixedSize(80, 80)
        self.play_button.clicked.connect(self.toggle_play_pause)

        self.control_bar.addWidget(self.play_button)

        # Add layouts to the main layout
        main_layout.addLayout(content_layout)
        main_layout.addLayout(self.control_bar)

        self.setLayout(main_layout)

        # Load Songs
        self.load_songs()

        # Play Song when clicked
        self.song_list.itemDoubleClicked.connect(self.play_song)

        # Window settings
        self.setWindowTitle('Music Player & Downloader')
        self.setGeometry(100, 100, 1400, 800)

#----------------------------------------------------------------------------------------------------------#

    def load_styles(self):
        """ Load external stylesheet """
        file = QFile("styles.css")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

#----------------------------------------------------------------------------------------------------------#

    def load_songs(self):
        """ Load available MP3 files from 'downloads' folder into the list """
        self.song_list.clear()
        self.download_dir = "C:/Music/downloads"
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)  # Create folder if it doesn't exist
        self.songs = [f for f in os.listdir(self.download_dir) if f.endswith(".mp3")]
        self.song_list.addItems(self.songs)  # Add song names to the list

#----------------------------------------------------------------------------------------------------------#

    def play_song(self):
        """ Play the selected song """
        selected_song = self.song_list.currentItem()
        if not selected_song:
            return  # No song selected
        
        song_path = os.path.join(self.download_dir, selected_song.text())

        if self.current_song == song_path:
            pygame.mixer.music.unpause()  # Resume if already paused
        else:
            pygame.mixer.music.load(song_path)  # Load new song
            pygame.mixer.music.play()
            self.current_song = song_path  # Update current song

#----------------------------------------------------------------------------------------------------------#

    def toggle_play_pause(self):
        """ Toggle play/pause and change the button icon """
        if pygame.mixer.music.get_busy():  
            pygame.mixer.music.pause()
            self.play_button.setIcon(QIcon("images/play.png"))  # Switch to play icon
        else:
            if not self.current_song:
                # If no song is playing, start playing the first song in the list
                if self.song_list.count() > 0:
                    self.song_list.setCurrentRow(0)  # Select first song
                    self.play_song()  # Play the selected song
            else:
                pygame.mixer.music.unpause()
                self.play_button.setIcon(QIcon("images/pause.png"))  # Switch to pause icon

#----------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MusicPlayerApp()
    ex.show()
    sys.exit(app.exec_())

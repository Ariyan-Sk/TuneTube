import sys
import os
import pygame
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QStackedWidget

class MusicPlayerApp(QWidget):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()  # Initialize pygame mixer
        self.current_song = None  # Keep track of the current song
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QHBoxLayout()

        # Sidebar (Navigation)
        self.sidebar = QListWidget()
        self.sidebar.addItem("🎵 Music Player")
        self.sidebar.addItem("📥 YouTube Downloader")
        self.sidebar.setFixedWidth(150)  # Sidebar width

        # Stack to hold different pages
        self.pages = QStackedWidget()

        # Music Player Page
        self.music_page = QWidget()
        self.music_layout = QVBoxLayout()  # Store in self to use later
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

        # Add sidebar and pages to the layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.pages)

        self.setLayout(main_layout)

        # Load Songs
        self.load_songs()

        # Play Song when clicked
        self.song_list.itemDoubleClicked.connect(self.play_song)

        # Window settings
        self.setWindowTitle('Music Player & Downloader')
        self.setGeometry(100, 100, 1400, 800)  # Set proper window size

    def load_songs(self):
        """ Load available MP3 files from 'downloads' folder into the list """
        self.song_list.clear()
        self.download_dir = "downloads"
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)  # Create folder if it doesn't exist
        self.songs = [f for f in os.listdir(self.download_dir) if f.endswith(".mp3")]
        self.song_list.addItems(self.songs)  # Add song names to the list

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MusicPlayerApp()
    ex.show()
    sys.exit(app.exec_())

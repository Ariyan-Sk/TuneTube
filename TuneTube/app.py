import sys
import os
import pygame
import yt_dlp
import ssl
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QStackedWidget, QPushButton, QSlider, QLineEdit, QProgressBar
from PyQt5.QtCore import QSize, QFile, QTextStream, Qt, QTimer
from PyQt5.QtGui import QIcon


ssl._create_default_https_context = ssl._create_unverified_context

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
        
        # Input field for YouTube URL
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL here...")
        download_layout.addWidget(self.url_input)
        
        # Download button
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_song)
        download_layout.addWidget(self.download_button)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        download_layout.addWidget(self.progress_bar)
        
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

        # Play/Pause Button
        self.play_button = QPushButton()
        self.play_button.setObjectName("playButton")
        self.play_button.setIcon(QIcon("images/play.png"))
        self.play_button.setIconSize(QSize(64, 64))
        self.play_button.setFixedSize(80, 80)
        self.play_button.clicked.connect(self.toggle_play_pause)
        self.control_bar.addWidget(self.play_button)

        # Volume Control Layout
        self.volume_layout = QVBoxLayout()
        self.volume_layout.setSpacing(2)

        # Volume Slider (Initially Hidden)
        self.volume_slider = QSlider(Qt.Vertical)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setFixedSize(50, 120)
        self.volume_slider.setStyleSheet("border: 2px solid #ddd; border-radius: 5px; background: white;")
        self.volume_slider.hide()
        self.volume_slider.valueChanged.connect(self.set_volume)

        # Volume Button
        self.volume_button = QPushButton()
        self.volume_button.setIcon(QIcon("images/volume.png"))
        self.volume_button.setIconSize(QSize(40, 40))
        self.volume_button.setFixedSize(50, 50)
        self.volume_button.setStyleSheet("border: none;")
        self.volume_button.clicked.connect(self.toggle_volume_slider)

        # Timer for hiding the slider
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.volume_slider.hide)

        # Add slider above the button
        self.volume_layout.addWidget(self.volume_slider)
        self.volume_layout.addWidget(self.volume_button)
        self.control_bar.addLayout(self.volume_layout)

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

    def toggle_play_pause(self):
        """ Toggle play/pause and change the button icon """
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.play_button.setIcon(QIcon("images/play.png"))
        else:
            pygame.mixer.music.unpause()
            self.play_button.setIcon(QIcon("images/pause.png"))

#----------------------------------------------------------------------------------------------------------#

    def toggle_volume_slider(self):
        """ Show/Hide volume slider above the button """
        if self.volume_slider.isVisible():
            self.volume_slider.hide()
        else:
            self.volume_slider.show()
            self.hide_timer.start(2000)  # Hide after 2 seconds

#----------------------------------------------------------------------------------------------------------#

    def set_volume(self, value):
        """ Set volume based on slider value """
        pygame.mixer.music.set_volume(value / 100.0)

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

    def download_song(self):
        """ Download a song from YouTube and update the song list """
        url = self.url_input.text().strip()
        if not url:
            self.download_status.setText("Please enter a valid YouTube URL.")
            return

        self.download_status.setText("Downloading...")
        
        os.makedirs("downloads", exist_ok=True)  # Ensure downloads folder exists

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save in 'downloads' folder
            'ffmpeg_location': r'C:\Users\ariyan.habibseikh\Downloads\ffmpeg-master-latest-win64-gpl-shared\bin'  # Adjust if needed
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.download_status.setText("Download Complete!")
            self.load_songs()  # Refresh song list
        except Exception as e:
            print("Error:", str(e))  # Print in console
            self.download_status.setText(f"Error: {str(e)}")


#----------------------------------------------------------------------------------------------------------#

    def update_progress(self, d):
        """ Update progress bar based on download status """
        if d['status'] == 'downloading':
            percent = d['_percent_str'].strip().replace('%', '')
            self.progress_bar.setValue(int(float(percent)))
        elif d['status'] == 'finished':
            self.progress_bar.setValue(100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MusicPlayerApp()
    ex.show()
    sys.exit(app.exec_())

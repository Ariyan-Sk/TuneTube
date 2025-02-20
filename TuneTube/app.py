import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QStackedWidget

class MusicPlayerApp(QWidget):
    def __init__(self):
        super().__init__()
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
        music_layout = QVBoxLayout()
        music_layout.addWidget(QLabel("🎵 Music Player Interface"))
        self.music_page.setLayout(music_layout)

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

        # Window settings
        self.setWindowTitle('Music Player & Downloader')
        self.setGeometry(100, 100, 1400, 800)  # Set proper window size

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MusicPlayerApp()
    ex.show()
    sys.exit(app.exec_())

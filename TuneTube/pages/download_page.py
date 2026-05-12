from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QProgressBar
)

from PyQt5.QtCore import pyqtSignal

from downloader import download_song as yt_download
from workers.download_worker import DownloadWorker

# ==========================================================
# DOWNLOAD PAGE
# ==========================================================

class DownloadPage(QWidget):

    # Emitted after a successful download so the
    # music page can refresh its song list
    download_complete = pyqtSignal()

    def __init__(self, download_dir):

        super().__init__()

        self.download_dir = download_dir

        layout = QVBoxLayout()

        layout.addWidget(QLabel("📥 YouTube Downloader"))

# URL INPUT

        self.url_input = QLineEdit()

        self.url_input.setPlaceholderText(
            "Paste YouTube URL..."
        )

        layout.addWidget(self.url_input)

# DOWNLOAD BUTTON

        self.download_button = QPushButton("Download")

        self.download_button.clicked.connect(
            self.handle_download
        )

        layout.addWidget(self.download_button)

# PROGRESS BAR

        self.progress_bar = QProgressBar()

        self.progress_bar.setValue(0)

        layout.addWidget(self.progress_bar)

# STATUS LABEL

        self.download_status = QLabel("")

        layout.addWidget(self.download_status)

        self.setLayout(layout)

# ==========================================================
# UPDATE PROGRESS BAR  (yt-dlp progress hook)
# ==========================================================

    def update_progress(self, d):

        if d['status'] == 'downloading':

            percent = (
                d.get('_percent_str', '0%')
                .replace('%', '')
                .strip()
            )

            try:
                self.progress_bar.setValue(
                    int(float(percent))
                )
            except:
                pass

        elif d['status'] == 'finished':

            self.progress_bar.setValue(100)

# ==========================================================
# HANDLE DOWNLOAD BUTTON
# ==========================================================

    def handle_download(self):

        url = self.url_input.text().strip()

        if not url:

            self.download_status.setText(
                "Enter a valid URL"
            )

            return

        self.progress_bar.setValue(0)

        self.download_button.setEnabled(False)

        # Create worker thread
        self.worker = DownloadWorker(url)

        # Connect signals
        self.worker.progress.connect(
            self.progress_bar.setValue
        )

        self.worker.status.connect(
            self.download_status.setText
        )

        self.worker.finished.connect(
            self.download_finished
        )

        # Start thread
        self.worker.start()

    
    def download_finished(self, success):

        self.download_button.setEnabled(True)

        if success:
            self.download_complete.emit()
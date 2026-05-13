import os

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)

from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QColor
from workers.download_worker import DownloadWorker

# ==========================================================
# HELPER FUNCTION
# ==========================================================

def _load_stylesheet(filename: str) -> str:

    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        filename
    )
    with open(path, "r") as f:
        return f.read()

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

        self.setStyleSheet(_load_stylesheet("download_page.qss"))

        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)

        layout.addWidget(QLabel("📥 YouTube Downloader"))

# LOADING ANIMATION  

        self.loader = QWebEngineView()

        loader_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "loader.html"
        )

        self.loader.load(
            QUrl.fromLocalFile(loader_path)
        )

        self.loader.setFixedHeight(300)
        self.loader.page().setBackgroundColor(QColor(0, 0, 0))

        layout.addWidget(self.loader)

        row = QHBoxLayout()
        row.setSpacing(10)
# URL INPUT

        self.url_input = QLineEdit()
        self.url_input.setObjectName("urlInput")      
        self.url_input.setPlaceholderText("Paste YouTube URL...")
        self.url_input.setFixedWidth(300)
        self.url_input.setFixedHeight(38)

# DOWNLOAD BUTTON

        self.download_button = QPushButton("Download")
        self.download_button.setObjectName("downloadButton") 
        self.download_button.setFixedHeight(38)
        self.download_button.setCursor(Qt.PointingHandCursor)
        self.download_button.clicked.connect(self.handle_download)
 
        row.addWidget(self.url_input)
        row.addWidget(self.download_button)
        row.addStretch()
 
        layout.addLayout(row)


# STATUS LABEL

        self.download_status = QLabel("")

        layout.addWidget(self.download_status)

        self.setLayout(layout)

# ==========================================================
# HELPER — run JS in the loader page
# ==========================================================

    def _set_loader_state(self, state: str):
        self.loader.page().runJavaScript(
            f"setState('{state}')"
        )

# ==========================================================
# HANDLE DOWNLOAD BUTTON
# ==========================================================

    def handle_download(self):

        self._set_loader_state("loading")

        self.download_status.setText("")

        url = self.url_input.text().strip()

        if not url:
            self.download_status.setText("Enter a valid URL")
            return

        self.download_button.setEnabled(False)

        # Create and wire up worker thread
        self.worker = DownloadWorker(url)

        # We no longer need progress % — just status text
        self.worker.status.connect(
            self.download_status.setText
        )

        self.worker.finished.connect(
            self.download_finished
        )

        self.worker.start()

# ==========================================================
# FINISHED CALLBACK
# ==========================================================

    def download_finished(self, success):

        self.download_button.setEnabled(True)

        if success:
            self._set_loader_state("complete")
            self.download_complete.emit()
        else:
            self._set_loader_state("failed")
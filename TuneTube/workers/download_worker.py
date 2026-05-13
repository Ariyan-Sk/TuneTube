from PyQt5.QtCore import (
    QThread,
    pyqtSignal
)

from downloader import download_song

import re

class DownloadWorker(QThread):

    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(bool)

    def __init__(self, url):
        super().__init__()

        self.url = url
        self.last_percent = -1

    # -----------------------------------------
    # yt-dlp progress hook
    # -----------------------------------------

    def update_progress(self, d):

        if d['status'] == 'downloading':

            percent_str = d.get(
                '_percent_str',
                '0%'
            )

            match = re.search(
                r'(\d+(\.\d+)?)',
                percent_str
            )

            if match:

                percent = round(
                    float(match.group(1))
                )

                if percent != self.last_percent:

                    self.last_percent = percent

                    print(percent)
                    
                    self.progress.emit(percent)
                    QThread.msleep(15)

        elif d['status'] == 'finished':

            self.progress.emit(100)

    # -----------------------------------------
    # thread main function
    # -----------------------------------------

    def run(self):

        self.status.emit("Downloading...")

        success = download_song(
            self.url,
            self.update_progress
        )

        if success:
            self.status.emit("Converting to MP3...")
            self.status.emit("Download Complete!")
        else:
            self.status.emit("Download Failed!")

        self.finished.emit(success)
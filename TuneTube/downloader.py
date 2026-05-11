import os
import yt_dlp


# --------------------------------------------------
# BASE FOLDERS
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DOWNLOAD_DIR = os.path.join(
    BASE_DIR,
    "downloads"
)

# FFmpeg folder path
# (point to the BIN folder, not directly ffmpeg.exe)

FFMPEG_PATH = os.path.join(
    BASE_DIR,
    "ffmpeg",
    "bin"
)


# --------------------------------------------------
# CREATE DOWNLOADS FOLDER IF MISSING
# --------------------------------------------------

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)


# --------------------------------------------------
# DOWNLOAD SONG FUNCTION
# --------------------------------------------------

def download_song(url, update_progress):

    # ----------------------------------------------
    # CLEAN URL
    # ----------------------------------------------

    url = url.strip()

    # Add https:// if user forgot it
    if not url.startswith("http"):
        url = "https://" + url

    # Remove playlist/radio parameters
    if "&list=" in url:
        url = url.split("&list=")[0]

    # Remove extra autoplay/radio parameters
    if "&start_radio=" in url:
        url = url.split("&start_radio=")[0]

    if "&pp=" in url:
        url = url.split("&pp=")[0]

    print("Clean URL:", url)

    # ----------------------------------------------
    # YT-DLP OPTIONS
    # ----------------------------------------------

    ydl_opts = {

        # Best audio
        'format': 'bestaudio/best',

        # Prevent playlist downloads
        'noplaylist': True,

        # Save file location
        'outtmpl': os.path.join(
            DOWNLOAD_DIR,
            '%(title)s.%(ext)s'
        ),

        # FFmpeg location
        'ffmpeg_location': FFMPEG_PATH,

        # Progress callback
        'progress_hooks': [
            update_progress
        ],

        # Convert to MP3
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],

        # Cleaner console
        'quiet': False,
        'no_warnings': False,
    }

    # ----------------------------------------------
    # DOWNLOAD
    # ----------------------------------------------

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            ydl.download([url])

        print("Download Complete")

        return True

    except Exception as e:

        print("Download Error:", e)

        return False
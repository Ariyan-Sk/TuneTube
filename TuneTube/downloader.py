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

        'format': 'bestaudio/best',

        'noplaylist': True,

        'outtmpl': os.path.join(
            DOWNLOAD_DIR,
            '%(title)s.%(ext)s'
        ),

        'ffmpeg_location': FFMPEG_PATH,

        'progress_hooks': [
            update_progress
        ],

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],

        'extractor_args': {
            'youtube': {
                'player_client': ['android']
            }
        },

        'quiet': False,
        'no_warnings': False,

        'overwrites': True,

        'retries': 10,
        'fragment_retries': 10,
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
import os
import yt_dlp
import requests
import zipfile
import sys

# Set up the downloads folder
DOWNLOAD_DIR = "C:/Music/downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# FFmpeg download details
FFMPEG_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
FFMPEG_DIR = os.path.join(DOWNLOAD_DIR, "ffmpeg")
FFMPEG_EXE = os.path.join(FFMPEG_DIR, "bin", "ffmpeg.exe")

def download_ffmpeg():
    """Download and extract FFmpeg if it's not already installed."""
    if os.path.exists(FFMPEG_EXE):
        print("FFmpeg already installed.")
        return FFMPEG_EXE

    print("Downloading FFmpeg...")
    zip_path = os.path.join(DOWNLOAD_DIR, "ffmpeg.zip")
    response = requests.get(FFMPEG_URL, stream=True)

    with open(zip_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)

    print("Extracting FFmpeg...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(FFMPEG_DIR)

    os.remove(zip_path)  # Cleanup

    # Locate the actual ffmpeg executable
    for root, dirs, files in os.walk(FFMPEG_DIR):
        if "ffmpeg.exe" in files:
            return os.path.join(root, "ffmpeg.exe")

    print("FFmpeg installation failed.")
    return None

def download_song(url, update_progress):
    """Download a YouTube song and save it as MP3."""
    if not url:
        print("Invalid URL")
        return False

    ffmpeg_path = download_ffmpeg()
    if not ffmpeg_path:
        print("FFmpeg setup failed.")
        return False

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': ffmpeg_path,
        'progress_hooks': [update_progress]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        print(f"Error downloading song: {e}")
        return False

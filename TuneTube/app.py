import sys
import ssl
 
from PyQt5.QtWidgets import QApplication
 
from main_window import MusicPlayerApp
 
 
# ==========================================================
# FIX SSL
# ==========================================================
 
ssl._create_default_https_context = (
    ssl._create_unverified_context
)
 
 
# ==========================================================
# RUN APP
# ==========================================================
 
if __name__ == '__main__':
 
    app = QApplication(sys.argv)
 
    window = MusicPlayerApp()
 
    window.show()
 
    sys.exit(app.exec_())
 
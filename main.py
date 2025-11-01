import sys
import os

# funciona melhor no sistema linux que testei, mas pode não precisar.
os.environ['QT_QPA_PLATFORM'] = 'xcb'

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from aether_editor.main_window import AetherEditorApp   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AetherEditorApp()
    window.show()
    sys.exit(app.exec())
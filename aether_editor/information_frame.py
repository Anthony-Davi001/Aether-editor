from PySide6.QtWidgets import(
    QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout, QSizePolicy
)

from PySide6.QtGui import(
    QIcon, QDesktopServices, QFont
)

from PySide6.QtCore import (
    QUrl, QSize, Qt
)

from .constants import H1,H2,H3,H4

class InformationFrame(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.main_layout=QVBoxLayout()
        self._setup_ui()
        self.setLayout(self.main_layout)

    def _setup_ui(self):
        label=QLabel(text="informações básicas:")
        label.setFont(H2)
        label.setStyleSheet("""color: white; font-weight: bold;""")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(label)

        autor=QLabel(text="Autor: Anthony Davi")
        autor.setFont(H4)
        autor.setStyleSheet("""color: white; font-weight: bold;""")
        autor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(autor)

        url_button=QPushButton(text="GitHub")
        url_button.setIcon(QIcon("aether_icon.png"))
        url_button.setIconSize(QSize(40, 40))
        url_button.clicked.connect(self.redirect_for)
        url_button.setStyleSheet("""
            QPushButton { 
                background-color: #413CD2; 
                color: white;
                border: 2px solid #413CD1;
                text-align: left;
                padding: 5px;
                font-size: 16pt;
            }
            QPushButton:hover {
                background-color: #3531AB;
                border: 2px solid white;
            }
        """)

        url_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.main_layout.addWidget(url_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addStretch()
        
    def redirect_for(self):
        QDesktopServices.openUrl(QUrl("https://github.com/Anthony-Davi001"))

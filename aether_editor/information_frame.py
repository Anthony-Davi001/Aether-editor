from PySide6.QtWidgets import(
    QWidget,
    QLabel, 
    QPushButton, 
    QVBoxLayout, 
    QSizePolicy
)

from PySide6.QtGui import(
    QIcon, 
    QDesktopServices, 
)

from PySide6.QtCore import (
    QUrl, 
    QSize, 
    Qt
)

from .constants import H1,H2,H3,H4

class InformationFrame(QWidget):
    """
    A widget (frame) that displays basic project information, such as the author and a link to GitHub.
    The frame uses a QVBoxLayout to organize a title, the author's name, and a redirect button.

    Args:
        parent (QWidget): The parent widget of this frame.
    """
    def __init__(self, parent: QWidget):
        super().__init__(parent=parent)
        self.main_layout=QVBoxLayout()
        self._setup_ui()
        self.setLayout(self.main_layout)

    def _setup_ui(self):
        """setup ui of information frame."""
        label=QLabel(text="informações básicas:")
        label.setFont(H2)
        label.setStyleSheet("""font-weight: bold;""")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(label)

        autor=QLabel(text="Autor: Anthony Davi")
        autor.setFont(H4)
        autor.setStyleSheet("""font-weight: bold;""")
        autor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(autor)

        url_button=QPushButton(text="GitHub")
        url_button.setIcon(QIcon("aether_icon.png"))
        url_button.setIconSize(QSize(40, 40))
        url_button.clicked.connect(lambda: self.redirect_for("https://github.com/Anthony-Davi001"))
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
        
    def redirect_for(self, link: str):
        """
        Opens the specified link in the user's default web browser.
        Uses QDesktopServices.openUrl to perform the redirection.

        Args:       
            link (str): The complete URL to which the user should be redirected.
        """
        QDesktopServices.openUrl(QUrl(link))

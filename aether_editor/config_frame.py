"""
Module containing the ConfigFrame class, which provides an interface for 
selecting and applying visual themes (CSS styles) to the application.
"""
from PySide6.QtWidgets import (
    QWidget, 
    QGridLayout, 
    QPushButton, 
    QSizePolicy, 
)

from .constants import set_css_style

class ConfigFrame(QWidget):
    """
    A configuration widget (frame) responsible for allowing the user to select and apply 
    different themes (CSS styles) to the application.
    The themes are arranged as buttons in a QGridLayout.
    """
    def __init__(self, parent: QWidget):
        """ 
        Initializes the ConfigFrame.

        Configures the main layout (QGridLayout) and calls the method to build the user interface.

        Args:
            parent (QWidget): The parent widget of this frame.
        """
        super().__init__(parent=parent)
        self.main_layout=QGridLayout()
        self.setLayout(self.main_layout)
        self._setup_ui()
    
    def _setup_ui(self):
        """
        Sets up the graphical elements of the configuration frame.

        It defines a list of available styles (name, CSS file, grid position) 
        and creates a QPushButton for each style. Each button's click signal 
        is connected to the set_css_style function to apply the corresponding 
        theme using its CSS file name.
        """
        styles=[
            {"style name": "Aether Style","css file name": "main_style.css","row": 0,"column": 0},
            {"style name": "Github Dark","css file name": "github_dark_style.css","row": 0,"column": 1},
            {"style name": "Github Light","css file name": "github_light_style.css","row": 0,"column": 2}
        ]
        for i in styles:
            button=QPushButton(text=i["style name"])
            button.setStyleSheet("""QPushButton{background-color: white;color: black;} QPushButton:hover{ border:4px solid purple; } QPushButton:pressed {background-color: gray;}""")
            button.setMaximumSize(200,100)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            css_file_name = i["css file name"]
            button.clicked.connect(lambda checked, filename=css_file_name: set_css_style(filename))
            self.main_layout.addWidget(button, i["row"], i["column"])


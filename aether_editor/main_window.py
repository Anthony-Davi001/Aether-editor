"""
main module of the Aether-editor, based in PySide6 (Qt for python)

contains the main class of the application, the AetherEditorApp, its a class inherited of QMainWindow
and contains all visual content of Aether Editor

Example:
    if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = AetherEditorApp() #<-- here!
        window.show()
        sys.exit(app.exec())
"""

import sys

from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QWidget,
    QTabWidget,
    QLabel
)

from .editor_frame import MarkdownEditorFrame
from .information_frame import InformationFrame
from .config_frame import ConfigFrame
from .constants import qss_style_sheet


class AetherEditorApp(QMainWindow):
    """
    window main class

    The layout, the core widgets, and the overall state of the graphical user interface (GUI) deserve it.
    This class acts as the main container for all application components, such as the code editor and the configuration section.
    """
    def __init__(self):
        """
        Initializes the main application window (QMainWindow).

        Sets the window title, size, and applies the global CSS stylesheet.
        It also sets up the QTabWidget as the central widget container.
        """
        super().__init__()
        self.setWindowTitle("Aether Editor - Editor de Markdown")
        self.setGeometry(100, 100, 1000, 700) 
        self.setStyleSheet(qss_style_sheet)

        self.tab_view=QTabWidget(parent=self)
        self.setCentralWidget(self.tab_view)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """
        Configures the user interface by creating and adding the main tabs.

        Creates instances of MarkdownEditorFrame, ConfigFrame, and InformationFrame,
        adding each as a new tab in the central widget (QTabWidget).
        """
        self.editor=self.create_new_tab(MarkdownEditorFrame, "Editor")
        self.configure_frame=self.create_new_tab(ConfigFrame, "Configurações")
        self.information=self.create_new_tab(InformationFrame, "Informações")

    def create_new_tab(self, widget_class: QWidget, text: str) -> QWidget:
        """
        Creates a new frame in the tabview with the desired class and name.

        Creates a new page in the tabview using a class inherited from the desired QWidget and adding the page with 
        the chosen name, and finally, returns the created instance after it has been placed in the tabview.

        Args:
            widget_class (QWidget): the frame class you want to add to the tabview
            text (str): the text that will appear in the window

        Returns:
            (QWidget): the QWidget instance that was created    
        """
        new_page=widget_class(parent=self.tab_view)
        self.tab_view.addTab(new_page, text)  
        return new_page  
    
    
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


class AetherEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aether Editor - Editor de Markdown (PySide6)")
        self.setGeometry(100, 100, 1000, 700) 

        self.tab_view=QTabWidget(parent=self)
        self.setCentralWidget(self.tab_view)
        self._setup_ui()
        
    def _setup_ui(self):
        self.editor=self.create_new_tab(MarkdownEditorFrame, "Editor")
        self.information=self.create_new_tab(InformationFrame, "Informações")

    def create_new_tab(self, widget_class: QWidget, text: str)->QWidget:
        """cria um novo frame na tabview com a classe e nome desejado
        
        cria uma nova página na tabview utilizando uma classe herdada de QWidget desejada e adicionando
        a página com o nome escolhido, e por fim, Retorna a instancia criada, após ter sido colocada na tabview
        
        Args:
            widget_class: a classe de frame que quer adicionar a tabview
            text: o texto que aparecerá na janela
            
        Returns:
            (QWidget): a instancia de QWidget que foi criada"""

        new_page=widget_class(parent=self.tab_view)
        self.tab_view.addTab(new_page, text)  
        return new_page  
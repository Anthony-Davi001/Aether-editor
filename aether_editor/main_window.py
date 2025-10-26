# main_window.py

import os
import markdown 

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QTextEdit, 
    QVBoxLayout, QPushButton, QFileDialog, QApplication, QToolBar
)
from PySide6.QtPrintSupport import QPrinter

from .code_editor import CodeEditor
from .constants import MARKDOWN_PREVIEW_STYLE

class MarkdownApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_filename = None
        self._setup_ui()
        self._set_initial_content()
        self.update_preview() 

    # --- Configuração de UI ---
    def _setup_ui(self):
        """Configura a interface gráfica da janela principal."""
        self.setWindowTitle("Aether Editor - Editor de Markdown (PySide6)")
        self.setGeometry(100, 100, 1000, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Painel Esquerdo (Editor + Toolbar)
        editor_v_layout = QVBoxLayout()
        
        toolbar = QToolBar("Ações")
        toolbar.setStyleSheet("background-color: #282c34; border: none;")
        toolbar.addWidget(self._create_button("Abrir MD", "#1d662e", self.open_markdown))
        toolbar.addWidget(self._create_button("Salvar MD", "#4e5cf8", self.save_markdown))
        toolbar.addWidget(self._create_button("Exportar PDF", "#5656f9", self.export_to_pdf))
        toolbar.addSeparator()

        editor_v_layout.addWidget(toolbar)
        
        self.editor = CodeEditor()
        self.editor.textChanged.connect(self.update_preview)
        editor_v_layout.addWidget(self.editor)
        main_layout.addLayout(editor_v_layout)

        # Painel Direito (Pré-visualização)
        self.preview = QTextEdit()
        self.preview.setReadOnly(True) 
        main_layout.addWidget(self.preview)
        
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 1)

    def _create_button(self, text, color, slot):
        """Função auxiliar para criar botões com estilo."""
        button = QPushButton(text)
        button.clicked.connect(slot)
        # Usando a cor de fundo e forçando o texto a ser preto para contraste com as cores primárias
        button.setStyleSheet(f"QPushButton{{background-color: {color}; color: white;}} QPushButton:hover{{border: 2px solid white;}}") 
        return button

    def _set_initial_content(self):
        """Define o texto inicial no editor."""
        initial_markdown = (
            """# Aether Editor - Por Anthony\n"""
            """\n"""
            """## Sobre o Código\n"""
            """* Este editor usa PySide6 para UI e `markdown` + `pygments` para o preview.\n"""
            """\n"""
            """```python\n"""
            """def fibonacci(n): \n"""
            """    # Este é um comentário\n"""
            """    a, b = 0, 1\n"""
            """    for _ in range(n):\n"""
            """        print("A string está em amarelo!")\n"""
            """        a, b = b, a + b\n"""
            """```\n"""
            """\n"""
            """| Cabeçalho 1 | Cabeçalho 2 |\n"""
            """| ----------- | ----------- |\n"""
            """| Célula A | Célula B |\n"""
            """| Célula C | Célula D |\n"""
        )
        self.editor.setPlainText(initial_markdown)

    # --- Funções de Manipulação de Arquivos e Lógica ---
    @Slot()
    def open_markdown(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Abrir Arquivo Markdown", "", "Arquivos Markdown (*.md *.markdown);;Todos os Arquivos (*)"
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.editor.setPlainText(f.read())
                self.current_filename = filename
                self.setWindowTitle(f"Aether Editor - {os.path.basename(filename)}")
            except Exception as e:
                print(f"Erro ao abrir arquivo: {e}")

    @Slot()
    def save_markdown(self):
        if not self.current_filename:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Salvar Arquivo Markdown", "documento.md", "Arquivos Markdown (*.md *.markdown);;Todos os Arquivos (*)"
            )
        else:
            filename = self.current_filename

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.editor.toPlainText())
                self.current_filename = filename
                self.setWindowTitle(f"Aether Editor - {os.path.basename(filename)}")
            except Exception as e:
                print(f"Erro ao salvar arquivo: {e}")

    @Slot()
    def export_to_pdf(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Salvar Documento PDF", "documento_markdown.pdf", "Arquivos PDF (*.pdf);;Todos os Arquivos (*)"
        )
        if filename:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(filename)
            self.preview.document().print_(printer)

    @Slot()
    def update_preview(self):
        """Converte Markdown para HTML com estilos e atualiza o preview."""
        markdown_text = self.editor.toPlainText()
        
        html_content = markdown.markdown(
            markdown_text, 
            extensions=['fenced_code', 'tables', 'codehilite']
        )
        
        # Injeta o CSS do constants.py no HTML
        styled_html = f"""
        <html>
        <head>
            <style>
                {MARKDOWN_PREVIEW_STYLE}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        self.preview.setHtml(styled_html)
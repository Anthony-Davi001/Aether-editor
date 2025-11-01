"""
Module containing the MarkdownEditorFrame class.

This class is a QWidget component that provides the core dual-pane interface 
for the Aether Editor, featuring a source Markdown text editor and a live, 
syntax-highlighted HTML preview pane.

It handles file operations (open, save, PDF export) and manages the debounced 
preview update logic using QTimer for efficient performance.
"""
import os

import markdown 
from PySide6.QtCore import Slot, QTimer
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QTextEdit,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QToolBar,
    QMessageBox, 
    QLabel
)

from PySide6.QtPrintSupport import QPrinter
from PySide6.QtGui import QTextCursor 
from typing import Callable, Any

from .code_editor import CodeEditor
from .constants import get_css_style

class MarkdownEditorFrame(QWidget):
    """
    Main component of the Markdown editor interface, providing the text editor 
    and the real-time HTML preview.

    The frame uses a QTimer for 'debounce' logic to delay the preview update, 
    optimizing performance during typing.

    Attributes:
        current_filename (str or None): The file path of the currently loaded Markdown file. None if no file is open.
        preview_timer (QTimer): The timer instance used to implement debouncing for the live preview update.
    """
    def __init__(self, parent: QWidget):
        """
        Initializes the Markdown editor frame, setting up the debounced preview
        timer and connecting signals.

        Args:
            parent (QWidget): the parent widget of this frame.
        """
        super().__init__(parent=parent)
        self.current_filename = None
        self.preview_timer = QTimer(self)
        
        self.preview_timer.setSingleShot(True) 
        self.preview_timer.setInterval(200) 
        self.preview_timer.timeout.connect(self.update_preview)

        self._setup_ui()
        self._set_initial_content()
        self.debounce_preview() 

    # --- ui config ---
    def _setup_ui(self)->None:
        """
        Configures the main dual-pane graphical user interface (GUI).

        The layout uses an QHBoxLayout to split the frame into two halves:
        the left side (editor_v_layout) contains the action toolbar and the 
        CodeEditor widget, and the right side contains the read-only QTextEdit 
        for the rendered preview. Stretches are set to ensure both panes take 
        equal space.
        """

        main_layout = QHBoxLayout(self)
        editor_v_layout = QVBoxLayout()
        
        toolbar = QToolBar("Ações")
        toolbar.setStyleSheet("background-color: #282c34; border: none;")
        toolbar.addWidget(self._create_button("Abrir MD", "#1d662e", self.open_markdown))
        toolbar.addWidget(self._create_button("Salvar MD", "#4e5cf8", self.save_markdown))
        toolbar.addWidget(self._create_button("Exportar PDF", "#5656f9", self.export_to_pdf))
        toolbar.addSeparator()
        self.save_status=QLabel(text="texto atualizado")
        toolbar.addWidget(self.save_status)

        editor_v_layout.addWidget(toolbar)
        
        self.editor = CodeEditor()
        self.editor.textChanged.connect(self.debounce_preview)
        editor_v_layout.addWidget(self.editor)
        main_layout.addLayout(editor_v_layout)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True) 
        main_layout.addWidget(self.preview)
        
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 1)
        
    def _create_button(self, text: str, color: str, function: Callable[...,Any]) -> QPushButton:
        """
        Creates a custom QPushButton and connects its action.

        This utility function reduces verbosity in the construction of the toolbar by applying a custom style.

        Args:
            text (str):The text to be displayed on the button.
            color (str): The background color of the button (in hexadecimal format, e.g., '#1d662e').
            function (Callable[...,Any]): The function or slot to be executed when the button is clicked.
        
        Returns:
            (QPushButton): customized button.
        """
        button = QPushButton(text)
        button.clicked.connect(function),
        button.setStyleSheet(f"QPushButton{{background-color: {color}; color: white;}} QPushButton:hover{{border: 2px solid white;}}") 
        return button

    def _set_initial_content(self)->None:
        """coloca o conteudo inicial do editor"""
        initial_markdown = (
            """# Aether Editor - Por Anthony\n"""
            """\n"""
            """## Sobre o Código\n"""
            """- Este editor usa PySide6 para UI e `markdown` + `pygments` para o preview (e pdf).\n"""
            """\n"""
            """```python\n"""
            """def fibonacci(n): \n"""
            """    # Este é um comentário\n"""
            """    a, b = 0, 1\n"""
            """    for i in range(n):\n"""
            """        print("Uma String")\n"""
            """        a, b = b, a + b\n"""
            """```\n"""
            """\n"""
            """```django+html\n"""
            """{% if form.errors %}\n"""
            """    <div>\n"""
            """        {% for error in form.errors %}\n"""
            """            <p>{{ error }}</p>\n"""
            """        {% enfor %}\n"""
            """    </div>\n"""
            """{% endif %}\n"""
            """```\n"""
            """| Cabeçalho 1 | Cabeçalho 2 |\n"""
            """| ----------- | ----------- |\n"""
            """| Célula A | Célula B |\n"""
            """| Célula C | Célula D |\n"""
        )
        self.editor.setPlainText(initial_markdown)

    # --- file methods ---
    @Slot()
    def open_markdown(self):
        """
        opens a Markdown file from the file system.

        Prompts the user for a file using QFileDialog, reads the contents into the editor,
        and updates the current file name and window title.
        """
        filename, _ = QFileDialog.getOpenFileName(
            self, "Abrir Arquivo Markdown", "", "Arquivos Markdown (*.md *.markdown);;Todos os Arquivos (*)"
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    self.editor.setPlainText(file.read())
                self.current_filename = filename
                self.setWindowTitle(f"Aether Editor - {os.path.basename(filename)}")

            except Exception as e:
                warning_message=QMessageBox()
                warning_message.setText(f"falha em abrir o arquivo\nErro: {e}")
                warning_message.setIcon(QMessageBox.Icon.Warning)
                warning_message.setStandardButtons(QMessageBox.StandardButton.Ok)
                warning_message.exec()

    @Slot()
    def save_markdown(self):
        """
        Saves the current editor content to the file.

        If "self.current_filename" is None, a QFileDialog opens so that
        the user can choose the name and location of the new file. Otherwise,
        the existing file is overwritten. Displays a QMessageBox indicating success or failure.
        """
        if not self.current_filename:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Salvar Arquivo Markdown", "documento.md", "Arquivos Markdown (*.md *.markdown);;Todos os Arquivos (*)"
            )
        else:
            filename = self.current_filename

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(self.editor.toPlainText())
                self.current_filename = filename
                self.setWindowTitle(f"Aether Editor - {os.path.basename(filename)}")

                success_message=QMessageBox()
                success_message.setText("salvamento efetuado com sucesso")
                success_message.setIcon(QMessageBox.Icon.Information)
                success_message.setStandardButtons(QMessageBox.StandardButton.Ok)
                success_message.exec()

            except Exception as e:
                warning_message=QMessageBox()
                warning_message.setText(f"falha no salvamento\nErro: {e}")
                warning_message.setIcon(QMessageBox.Icon.Warning)
                warning_message.setStandardButtons(QMessageBox.StandardButton.Ok)
                warning_message.exec()

    @Slot()
    def export_to_pdf(self):
        """
        Exports the rendered preview content to a PDF file.

        Opens a QFileDialog for the user to select the file location and name.
        Uses QPrinter in high-resolution mode to convert the displayed HTML document to PDF.
        """
        filename, _ = QFileDialog.getSaveFileName(
            self, "Salvar Documento PDF", "documento_markdown.pdf", "Arquivos PDF (*.pdf);;Todos os Arquivos (*)"
        )
        if filename:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(filename)
            self.preview.document().print_(printer)

    @Slot()
    def debounce_preview(self):
        """
        Schedules the execution of the preview update.

        Cancels any pending execution and starts the QTimer. The timer only triggers the heavy code if 
        it is not restarted (i.e., if the user stops typing).
        """
        self.save_status.setText("atualizando texto...")
        self.preview_timer.start()

    @Slot()
    def update_preview(self):
        """
        Converts Markdown text from the editor to styled HTML and updates the preview.

        The conversion process uses the markdown module with the extensions
        'fenced_code', 'tables', and 'codehilite' for code block support
        and syntax highlighting. The style is injected with get_css_style().
        """
        markdown_text = self.editor.toPlainText()
        
        html_content = markdown.markdown(
            markdown_text, 
            extensions=['fenced_code', 'tables', 'codehilite']
        )
        
        styled_html = f"""
        <html>
        <head>
            <style>
                {get_css_style()}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        self.preview.setHtml(styled_html)
        self.save_status.setText("texto atualizado")

        cursor = self.preview.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End) 
        self.preview.setTextCursor(cursor)
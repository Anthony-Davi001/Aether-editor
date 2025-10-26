# code_editor.py

from PySide6.QtCore import Qt, QRect, QSize, Slot
from PySide6.QtGui import (
    QColor, QFont, QPainter, QTextCharFormat, QTextCursor
)
from PySide6.QtWidgets import (
    QWidget, QPlainTextEdit, QTextEdit
)

from .constants import (
    LINE_NUMBER_BG_COLOR, LINE_NUMBER_TEXT_COLOR, HIGHLIGHT_LINE_COLOR
)

class LineNumberArea(QWidget):
    """Widget auxiliar para desenhar os números das linhas."""
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
    """QPlainTextEdit personalizado com numeração de linhas e destaque da linha atual."""
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.lineNumberArea = LineNumberArea(self)
        
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        
        font = QFont("Consolas")
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

    # --- Métodos de Geometria ---
    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    @Slot(int)
    def updateLineNumberAreaWidth(self, newBlockCount):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    @Slot(QRect, int)
    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(
            cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()
        ))

    # --- Métodos de Desenho e Destaque ---
    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), LINE_NUMBER_BG_COLOR) 

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(LINE_NUMBER_TEXT_COLOR) 
                
                painter.drawText(
                    0, top, 
                    self.lineNumberArea.width(), 
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight, 
                    number
                )
            
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    @Slot()
    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection() 
            selection.format.setBackground(HIGHLIGHT_LINE_COLOR)
            selection.format.setProperty(QTextCharFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        
        self.setExtraSelections(extraSelections)
from PySide6.QtCore import (
    Qt, 
    QRect, 
    QSize, 
    Slot
)
from PySide6.QtGui import (
    QColor, 
    QFont,
    QPainter, 
    QTextCharFormat, 
    QPalette,
    QSyntaxHighlighter,
)
from PySide6.QtWidgets import (
    QWidget, 
    QPlainTextEdit, 
    QTextEdit
)
from PySide6.QtCore import Qt
import re

class MarkdownHighlighter(QSyntaxHighlighter):
    """
    Custom syntax highlighter (QSyntaxHighlighter) for Markdown.

    This class applies syntax highlighting to Markdown elements, such as headings, bold, italics,
    and lists. The highlighting uses regular expressions for single-line rules. For multi-line code blocks (enclosed by ```),
    the QSyntaxHighlighter's state logic is used, applying a specific text color format to distinguish the code.

    Attributes:
        highlighting_rules (list): Single-line highlighting rules (Regex and format).
        code_block_format (QTextCharFormat): Format for multi-line code blocks (text color only).
    """
    STATE_NORMAL = 0
    STATE_CODE = 1
    def __init__(self, parent):
        super().__init__(parent)
        self._setup_styles()
        self.highlighting_rules = []
        self._setup_rules()
        

    def _setup_styles(self):
        """
        Defines and initializes all QTextCharFormat objects used for highlighting.

        Colors are fixed and designed for a dark theme. Includes formats for headings, 
        bold, italics, quotes, lists, inline code, and code blocks.
        """
        # 1. header (#)
        self.header_format = QTextCharFormat()
        self.header_format.setForeground(QColor("#A18CFD")) 
        self.header_format.setFontWeight(QFont.Bold)
        
        # 2. bold (**)
        self.bold_format = QTextCharFormat()
        self.bold_format.setForeground(QColor("#F08000"))
        self.bold_format.setFontWeight(QFont.Bold)
        
        # 3. italic (*)
        self.italic_format = QTextCharFormat()
        self.italic_format.setForeground(QColor("#F08000"))
        self.italic_format.setFontItalic(True)
        
        # 4. quote (>)
        self.quote_format = QTextCharFormat()
        self.quote_format.setForeground(QColor("#9E9E9E")) 
        
        # 5. list (*, 1., etc.)
        self.list_format = QTextCharFormat()
        self.list_format.setForeground(QColor("#81FF9C"))
        
        # 6. inline code (`)
        self.code_inline_format = QTextCharFormat()
        self.code_inline_format.setForeground(QColor("#FF5722"))
        self.code_inline_format.setBackground(QColor("#1e1e1e"))
        
        # 7. code_multiline (```)
        self.code_block_format = QTextCharFormat()
        self.code_block_format.setForeground(QColor("#81F7DD"))

        # default text format
        self.default_text_format = QTextCharFormat()
        self.default_text_format.setForeground(QColor("#D0D0D0"))

    def _setup_rules(self):
        """Define as regras Regex para realce de linha única."""
        self.highlighting_rules.append(
            (re.compile(r"^\s*(\*|\-|\+|\d+\.)\s+.*"), self.list_format)
        )
        self.highlighting_rules.append((re.compile(r'^#+\s.*'), self.header_format)) 
        self.highlighting_rules.append((re.compile(r'(\*\*|__)(.+?)(\*\*|__)'), self.bold_format))
        self.highlighting_rules.append((re.compile(r'(\*|_)(.+?)(\*|_)'), self.italic_format))
        self.highlighting_rules.append((re.compile(r'^>\s.*'), self.quote_format))
        self.highlighting_rules.append((re.compile(r'`[^`]+`'), self.code_inline_format))
        
        self.start_code_block_exp = re.compile(r"^\s*`{3}")
        self.end_code_block_exp = re.compile(r"`{3}\s*$")

    def highlightBlock(self, text: str):
        """
        Applies syntax highlighting to the provided text block (line).

        Highlighting occurs in two phases: applying single-line rules
        (Regex) and managing state for multi-line blocks.

        1. **Single-Line Rules (Regex):** Elements such as headings, lists,
        bold, italics, and inline code are formatted independently
        of the previous block's state.

        2. **Multi-Line Block Management (State):** The method uses the state
        of the previous block (`previousBlockState()`) and sets the state of the current block (`setCurrentBlockState()`) to track the extent of code blocks
        (delimited by ```). The state allows the code block highlighting to extend over multiple lines.

        Args:
            text: The text string of the current block (line) to be processed.
        """
        for expression, format in self.highlighting_rules:
            for match in expression.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), format)
        
        current_state = self.previousBlockState()
        index = 0
        
        while index < len(text):
            
            if current_state == self.STATE_CODE:
                end_match = self.end_code_block_exp.search(text, index)
                
                if end_match:
                    self.setFormat(0, end_match.end(), self.code_block_format)
                    current_state = self.STATE_NORMAL
                    index = end_match.end()
                    continue 

                else:
                    self.setFormat(0, len(text), self.code_block_format)
                    break 
            
            else:
                start_match = self.start_code_block_exp.search(text, index)
                
                if start_match:
                    start_pos = start_match.start()
                    index = start_match.end()
                    
                    end_match = self.end_code_block_exp.search(text, index)
                    
                    if end_match:
                        self.setFormat(start_pos, end_match.end() - start_pos, self.code_block_format)
                        index = end_match.end()
                        current_state = self.STATE_NORMAL
                    else:
                        self.setFormat(start_pos, len(text) - start_pos, self.code_block_format)
                        current_state = self.STATE_CODE 
                        break

                else:
                    break 
        
        self.setCurrentBlockState(current_state)

class LineNumberArea(QWidget):
    """
    Auxiliary widget for drawing line numbers.

    This widget is inserted in the left margin of the CodeEditor and is responsible
    only for rendering line numbers. It does not contain text editing logic.

    Attributes:
        code_editor (CodeEditor): Reference to the main instance of the editor.
    """
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor
        self.setAutoFillBackground(True)


    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    """
    Customized QPlainTextEdit with line numbering and current line highlighting.

    This class extends QPlainTextEdit to add crucial functionalities
    to a code editor: persistent line numbering and a visual highlight
    for the line where the cursor is positioned.

    Attributes:
        line_number_area (LineNumberArea): The helper widget for displaying line numbers.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighter = MarkdownHighlighter(self.document())
        self.setObjectName("CodeEditor")
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        
        self.line_number_area = LineNumberArea(self)
        self.line_number_area.setObjectName("lineNumberArea")
        
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        
        font = QFont("Consolas")
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)

        self.update_line_number_area_width(0)
        self.highlight_current_line()

   
    def line_number_area_width(self):
        """
        Calculates the required width for the line numbering widget.

        The width is based on the total number of blocks (lines) and adjusted 
        dynamically to ensure space for the maximum line number.

        Returns:
            int: The width in pixels required to display the line numbers.
        """

        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        
        space = 9 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    @Slot(int)
    def update_line_number_area_width(self, new_block_count: int):
        """
        Updates the editor viewport margins to accommodate line numbering.

        This method is connected to the "blockCountChanged" signal and 
        ensures that the left margin is always wide enough.

        Args:
            new_block_count(int): The new total number of blocks (lines), although the actual value of the argument is not consumed, only the method call.
        """
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    @Slot(QRect, int)
    def update_line_number_area(self, rect, dy):
        """
        Updates the line numbering widget (redraws or scrolls).

        This slot is connected to the "updateRequest" signal of QPlainTextEdit, optimizing
        the redraw. If there is vertical scrolling (dy != 0), the widget is scrolled
        instead of redrawn.

        Args:
            rect (QRect): The area that needs updating (in viewport coordinates).
            dy (int): The vertical scroll offset.
        """
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        """
        Window resize event handler.

        Ensures that the "lineNumberArea" widget always remains on the left margin
        and extends to the full height of the editor.

        Args:
            event (QResizeEvent): The received resize event.
        """
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(
            cr.left(), cr.top(), self.line_number_area_width(), cr.height()
        ))

    
    def line_number_area_paint_event(self, event):
        """
        Draws line numbers in the "LineNumberArea" widget.

        This is the primary rendering method. It iterates over the visible 
        blocks and draws their line numbers, separating them with a vertical line.

        Arguments:
            event (QPaintEvent): The paint event triggered by "LineNumberArea".
        """
        painter = QPainter(self.line_number_area)
        bg_color = self.line_number_area.palette().color(QPalette.ColorRole.Window)
        painter.fillRect(event.rect(), bg_color) 

        border_color_prop = self.line_number_area.palette().color(QPalette.ColorRole.WindowText)
        painter.setPen(border_color_prop)
        
        x_pos = self.line_number_area.width() - 2
        painter.drawLine(x_pos, event.rect().top(), x_pos, event.rect().bottom())

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()


        text_color = self.line_number_area.palette().color(QPalette.ColorRole.WindowText)

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)+" "
                painter.setPen(text_color) 
                
                painter.drawText(
                    0, top, 
                    self.line_number_area.width(), 
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight, 
                    number
                )
            
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    @Slot()
    def highlight_current_line(self):
        """
        Highlights the line of text where the cursor is positioned.

        This slot is connected to the "cursorPositionChanged" signal. It creates an
        "ExtraSelection" using the current theme's highlight color and applies it
        to the line where the cursor is.
        """
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection() 
            highlight_color = self.palette().color(QPalette.ColorRole.Highlight)
            selection.format.setBackground(highlight_color)
            selection.format.setProperty(QTextCharFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        
        self.setExtraSelections(extraSelections)
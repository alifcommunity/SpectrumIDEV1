from PyQt6.QtWidgets import QPlainTextEdit, QFrame
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QRect
import AlifSyntax
import random


#######################################################  تعريف المحرر ##################################################

class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = BarNum(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.highlight = AlifSyntax.AlifHighlighter(self.document())
        codeOpt = self.document().defaultTextOption()
        codeOpt.setAlignment(Qt.AlignmentFlag.AlignRight)
        codeOpt.setTextDirection(Qt.LayoutDirection.RightToLeft)
        self.document().setDefaultTextOption(codeOpt)
        self.setStyleSheet("background-color: #27292D ;color: #fff;font: 12pt Tajawal; border: 30px; border-radius: 7px; border-color: #fff; padding: 6px;")
        self.setTabStopDistance(16)
        self.openExample()

    def openExample(self):
        with open("./Example/جمع.alif", "r", encoding="utf-8") as example:
            exampleRead = example.read()
            self.setPlainText(exampleRead)
            example.close()

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.document().blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(0, 0, self.lineNumberAreaWidth() + 20, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberAreaWidth(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(cr.right() - self.lineNumberAreaWidth() - 3, cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def PaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                randcolor = lambda: random.randint(150,200)
                painter.setPen(QColor("#%02X%02X%02X" % (randcolor(),randcolor(),randcolor())))
                painter.drawText(0, int(top), self.lineNumberArea.width(), height, Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

class BarNum(QFrame):
    def __init__(self, editor):
        super().__init__(editor)
        self.code = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.code.PaintEvent(event)

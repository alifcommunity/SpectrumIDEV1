from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFrame, QTextEdit, QApplication, QSizeGrip, QFileDialog, QPlainTextEdit
from PyQt6.QtCore import QSize, Qt, QMetaObject, QCoreApplication, QPointF, QRect
from PyQt6.QtGui import QIcon, QPixmap, QColor, QPainter
from PyQt6 import sip
import subprocess
import sys
import os
import time
import alif_syn_pars

#######################################################################################################################

class BarNum(QFrame):
    def __init__(self, editor):
        super().__init__(editor)
        self.code = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.code.PaintEvent(event)

class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = BarNum(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.highlight = alif_syn_pars.PythonHighlighter(self.document())
        txtOpt = self.document().defaultTextOption()
        txtOpt.setAlignment(Qt.AlignmentFlag.AlignRight)
        txtOpt.setTextDirection(Qt.LayoutDirection.RightToLeft)
        self.document().setDefaultTextOption(txtOpt)
        self.setStyleSheet("background-color: rgb(39, 41, 45);color: rgb(255, 255, 255);font: 12pt \"Tajawal\";border : 30px;border-radius: 10px;border-color: rgb(255, 255, 255); padding: 6px;")
        self.setTabStopDistance(16)

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
        self.lineNumberArea.setGeometry(QRect(cr.right() - self.lineNumberAreaWidth() - 3, cr.top(), self.lineNumberAreaWidth(), cr.height()))

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
                painter.setPen(QColor("#BABABA"))
                painter.drawText(0, int(top), self.lineNumberArea.width(), height, Qt.AlignmentFlag.AlignCenter, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1


class Ui_MainWin(object):

    def setupUi(self, MainWin):
        MainWin.setGeometry(0, 0, 1280, 720)
        MainWin.setMinimumSize(QSize(900, 500))
        MainWin.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.mainwind = QWidget(MainWin)
        self.mainwind.setStyleSheet("background-color: \"#1c1d20\";border-radius: 10px")

        self.vMainWindLay = QVBoxLayout(self.mainwind)
        self.vMainWindLay.setContentsMargins(0, 0, 0, 0)
        self.vMainWindLay.setSpacing(0)

        self.topbarfrm = QFrame(self.mainwind)
        self.topbarfrm.setMinimumHeight(45)
        self.topbarfrm.setMaximumHeight(45)
        self.topbarfrm.setStyleSheet("background-color: \"#1c1d20\";")
        self.topbarfrm.mousePressEvent = self.mousePressEvent
        self.topbarfrm.mouseMoveEvent = self.mouseMoveEvent
        self.topbarfrm.mouseReleaseEvent = self.mouseReleaseEvent

        self.hTopBarfrmLay = QHBoxLayout(self.topbarfrm)
        self.hTopBarfrmLay.setContentsMargins(3, 0, 3, 0)
        self.hTopBarfrmLay.setSpacing(0)

        self.logofrm = QFrame(self.topbarfrm)
        self.logofrm.setMaximumWidth(90)

        self.hLogofrmLay = QHBoxLayout(self.logofrm)
        self.hLogofrmLay.setContentsMargins(43, 3, 0, 0)
        self.hLogofrmLay.setSpacing(0)

        self.alifBtn = QPushButton(self.logofrm)
        self.alifBtn.setFixedHeight(40)
        self.alifBtn.setFixedWidth(40)
        self.alifBtn.setStyleSheet("background-color: \"#1c1d20\";border: 0px")
        self.alifBtn.setIcon(QIcon("./icons/Alif.ico"))
        self.alifBtn.setIconSize(QSize(25, 25))

        self.hLogofrmLay.addWidget(self.alifBtn)
        self.hTopBarfrmLay.addWidget(self.logofrm)

        self.titlefrm = QFrame(self.topbarfrm)

        self.hTitlefrmLay = QHBoxLayout(self.titlefrm)
        self.hTitlefrmLay.setContentsMargins(0, 0, 0, 0)
        self.hTitlefrmLay.setSpacing(0)

        self.title = QLabel(self.titlefrm)
        self.title.setStyleSheet("font: 11pt \"Tajawal\";color: \"#fff\"")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hTitlefrmLay.addWidget(self.title)
        self.hTopBarfrmLay.addWidget(self.titlefrm)

        self.controlwinfrm = QFrame(self.topbarfrm)
        self.controlwinfrm.setMaximumWidth(90)

        self.hControlWinfrmLay = QHBoxLayout(self.controlwinfrm)
        self.hControlWinfrmLay.setContentsMargins(0, 0, 0, 0)
        self.hControlWinfrmLay.setSpacing(0)

        self.minimizeBtn = QPushButton(self.controlwinfrm)
        self.minimizeBtn.setFixedHeight(25)
        self.minimizeBtn.setFixedWidth(25)
        self.minimizeBtn.setStyleSheet("QPushButton{background-color: \"#1c1d20\";border: 0px;border-radius: 3px;}QPushButton:hover{background-color:  rgb(73, 85, 255);}QPushButton:pressed{background-color: rgb(50, 58, 175);}")
        self.minimizeBtn.setIcon(QIcon("./icons/Minimize.png"))
        self.minimizeBtn.setIconSize(QSize(13, 13))
        self.minimizeBtn.clicked.connect(MainWin.showMinimized)

        self.hControlWinfrmLay.addWidget(self.minimizeBtn)

        self.maximizeBtn = QPushButton(self.controlwinfrm)
        self.maximizeBtn.setFixedWidth(25)
        self.maximizeBtn.setFixedHeight(25)
        self.maximizeBtn.setStyleSheet("QPushButton{background-color: \"#1c1d20\";border: 0px;border-radius: 3px;}QPushButton:hover{background-color:  rgb(73, 85, 255);}QPushButton:pressed{background-color: rgb(50, 58, 175);}")
        self.maximizeBtn.setIcon(QIcon("./icons/Maximize.png"))
        self.maximizeBtn.setIconSize(QSize(13, 13))
        self.maximizeBtn.clicked.connect(self.restore)

        self.hControlWinfrmLay.addWidget(self.maximizeBtn)

        self.closeBtn = QPushButton(self.controlwinfrm)
        self.closeBtn.setFixedHeight(25)
        self.closeBtn.setFixedWidth(25)
        self.closeBtn.setStyleSheet("QPushButton{background-color: \"#1c1d20\";border: 0px;border-radius: 3px;}QPushButton:hover{background-color: rgb(218, 0, 0);}QPushButton:pressed{background-color: rgb(50, 58, 175);}")
        self.closeBtn.setIcon(QIcon("./icons/Close.png"))
        self.closeBtn.setIconSize(QSize(13, 13))
        self.closeBtn.clicked.connect(MainWin.close)

        self.hControlWinfrmLay.addWidget(self.closeBtn)
        self.hTopBarfrmLay.addWidget(self.controlwinfrm)
        self.vMainWindLay.addWidget(self.topbarfrm)

        self.mainfrm = QFrame(self.mainwind)
        self.mainfrm.setStyleSheet("background-color: \"#1c1d20\";")

        self.hMainfrmLay = QHBoxLayout(self.mainfrm)
        self.hMainfrmLay.setContentsMargins(0, 0, 0, 0)
        self.hMainfrmLay.setSpacing(0)

        self.menufrm = QFrame(self.mainfrm)
        self.menufrm.setFixedWidth(50)
        self.menufrm.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.menufrm.setStyleSheet("background-color: \"#1c1d20\";")

        self.vMenufrmLay = QVBoxLayout(self.menufrm)
        self.vMenufrmLay.setContentsMargins(0, 3, 0, 30)
        self.vMenufrmLay.setSpacing(0)

        self.topbtnsfrm = QFrame(self.menufrm)

        self.vTopBtnsfrmLay = QVBoxLayout(self.topbtnsfrm)
        self.vTopBtnsfrmLay.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vTopBtnsfrmLay.setContentsMargins(0, 0, 5, 0)
        self.vTopBtnsfrmLay.setSpacing(6)

        self.newBtn = QPushButton(self.topbtnsfrm)
        self.newBtn.setFixedWidth(40)
        self.newBtn.setFixedHeight(40)
        self.newBtn.setStyleSheet("QPushButton{background-color: \"#1c1d20\";color: rgb(255, 255, 255);border: 0px;border-radius: 6px;}QPushButton:hover{background-color:  rgb(73, 85, 255);}QPushButton:pressed{background-color: rgb(50, 58, 175);}")
        self.newBtn.setIcon(QIcon("./icons/New.png"))
        self.newBtn.setIconSize(QSize(25, 25))
        self.newBtn.clicked.connect(self.new)

        self.vTopBtnsfrmLay.addWidget(self.newBtn)

        self.openBtn = QPushButton(self.topbtnsfrm)
        self.openBtn.setFixedWidth(40)
        self.openBtn.setFixedHeight(40)
        self.openBtn.setStyleSheet("QPushButton{background-color: \"#1c1d20\";color: rgb(255, 255, 255);border: 0px;border-radius: 6px;}QPushButton:hover{background-color:  rgb(73, 85, 255);}QPushButton:pressed{background-color: rgb(50, 58, 175);}")
        self.openBtn.setIcon(QIcon("./icons/Open.png"))
        self.openBtn.setIconSize(QSize(25, 25))
        self.openBtn.clicked.connect(self.open)

        self.vTopBtnsfrmLay.addWidget(self.openBtn)

        self.saveBtn = QPushButton(self.topbtnsfrm)
        self.saveBtn.setFixedHeight(40)
        self.saveBtn.setFixedWidth(40)
        self.saveBtn.setStyleSheet("QPushButton{background-color: \"#1c1d20\";color: rgb(255, 255, 255);border: 0px;border-radius: 6px;}QPushButton:hover{background-color:  rgb(73, 85, 255);}QPushButton:pressed{background-color: rgb(50, 58, 175);}")
        self.saveBtn.setIcon(QIcon("./icons/Save.png"))
        self.saveBtn.setIconSize(QSize(25, 25))
        self.saveBtn.clicked.connect(self.save)

        self.vTopBtnsfrmLay.addWidget(self.saveBtn)
        self.vMenufrmLay.addWidget(self.topbtnsfrm)

        self.runbtnfrm = QFrame(self.menufrm)

        self.vRunBtnfrmLay = QVBoxLayout(self.runbtnfrm)
        self.vRunBtnfrmLay.setContentsMargins(0, 0, 5, 3)
        self.vRunBtnfrmLay.setSpacing(0)

        self.runBtn = QPushButton(self.runbtnfrm)
        self.runBtn.setFixedWidth(40)
        self.runBtn.setFixedHeight(40)
        self.runBtn.setStyleSheet("QPushButton{background-color:\"#1c1d20\";color: rgb(255, 255, 255);border: 0px;border-radius: 6px;}QPushButton:hover{background-color:rgb(246, 255, 67);}QPushButton:pressed{background-color: rgb(223, 227, 0);}")
        self.runBtn.setIcon(QIcon("./icons/Run.png"))
        self.runBtn.setIconSize(QSize(25, 25))
        self.runBtn.clicked.connect(self.run)

        self.vRunBtnfrmLay.addWidget(self.runBtn)
        self.vRunBtnfrmLay.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.vMenufrmLay.addWidget(self.runbtnfrm)
        self.hMainfrmLay.addWidget(self.menufrm)

        self.codefrm = QFrame(self.mainfrm)

        self.vCodefrmLay = QVBoxLayout(self.codefrm)
        self.vCodefrmLay.setContentsMargins(6, 0, 0, 6)

        self.code = CodeEditor(self.codefrm)

        self.vCodefrmLay.addWidget(self.code)

        self.result = QTextEdit(self.codefrm)
        self.result.setReadOnly(True)
        self.result.setFixedHeight(150)
        self.result.setStyleSheet("background-color:rgb(10, 11, 12);color: rgb(255, 255, 255);font: 12pt \"Tajawal\";border: 0px;border-radius: 10px;")

        self.vCodefrmLay.addWidget(self.result)

        self.statusbar = QFrame(self.codefrm)
        self.statusbar.setFixedHeight(20)
        self.statusbar.setStyleSheet("background-color: rgb(28, 29, 32);border-radius: 10px;")

        self.horizontalLayout = QHBoxLayout(self.statusbar)
        self.horizontalLayout.setContentsMargins(3, 0, 0, 0)

        self.statusLable = QLabel(self.statusbar)
        self.statusLable.setStyleSheet("color: rgb(190, 190, 190);font: 9pt \"Tajawal\"")
        self.statusLable.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout.addWidget(self.statusLable)

        self.resizeGrip = QSizeGrip(self.statusbar)
        self.resizeGrip.setFixedWidth(15)
        self.resizeGrip.setFixedHeight(15)
        self.resizeLable = QLabel(self.resizeGrip)
        self.resizeLable.setPixmap(QPixmap("./icons/Resize.png"))

        self.horizontalLayout.addWidget(self.resizeGrip)
        self.vCodefrmLay.addWidget(self.statusbar)
        self.hMainfrmLay.addWidget(self.codefrm)
        self.vMainWindLay.addWidget(self.mainfrm)

        MainWin.setCentralWidget(self.mainwind)
        self.retranslateUi(MainWin)
        QMetaObject.connectSlotsByName(MainWin)

        QFileDialog.setWindowIcon(MainWin, QIcon("./icons/Alif.png"))
        self.fileOpened = False
        self.fileSaved = False
        self.file_name = None

#######################################################################################################################

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.m_flag = True
            MainWin.m_Position = QPointF.toPoint(event.globalPosition()) - MainWin.pos()

    def mouseMoveEvent(self, QMouseEvent):
        if MainWin.isMaximized():
            self.maximizeBtn.setIcon(QIcon("./icons/Maximize.png"))
            self.mainwind.setStyleSheet("background-color: \"#1c1d20\";border-radius: 10px")
            MainWin.showNormal()
        if Qt.MouseButton.LeftButton and self.m_flag:
            MainWin.move(QPointF.toPoint(QMouseEvent.globalPosition()) - MainWin.m_Position)

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False

    def restore(self):
        if MainWin.isMaximized():
            self.maximizeBtn.setIcon(QIcon("./icons/Maximize.png"))
            MainWin.showNormal()
            self.mainwind.setStyleSheet("background-color: \"#1c1d20\";border-radius: 10px")
        else:
            self.maximizeBtn.setIcon(QIcon("./icons/Restore.png"))
            MainWin.showMaximized()
            self.mainwind.setStyleSheet("background-color: #1c1d20")

    def new(self):
        self.save()
        self.code.clear()
        self.result.clear()
        self.fileOpened = False
        self.fileSaved = False
        self.file_name = None

    def open(self):
        try:
            self.file_name, _ = QFileDialog.getOpenFileName(MainWin, "فتح ملف ألف", "", "كل الملفات (*.alif)")
            with open(self.file_name, "r", encoding="utf-8") as openFile:
                fileCode = openFile.read()
                self.code.setPlainText(fileCode)
                openFile.close()
            self.fileOpened = True
        except:
            pass

    def save(self):
        try:
            code = self.code.toPlainText()
            if self.fileOpened:
                with open(self.file_name, "w", encoding="utf-8") as saveFile:
                    saveFile.write(code)
                    saveFile.close()
            elif self.fileSaved:
                with open(self.file_name, "w", encoding="utf-8") as saveFile:
                    saveFile.write(code)
                    saveFile.close()
            else:
                self.file_name, _ = QFileDialog.getSaveFileName(MainWin, "حفظ ملف ألف", "غير معنون.alif", "ملف ألف (*.alif)")
                with open(self.file_name, "w", encoding="utf-8") as saveFile:
                    saveFile.write(code)
                    saveFile.close()
                self.fileSaved = True
        except:
            pass

    def run(self):
        fileDir = "Temp"
        if not os.path.exists(fileDir):
            os.mkdir(fileDir)
        else:
            pass

        start_time = time.time()
        code = self.code.toPlainText()

        with open(os.path.join(fileDir, "temp.alif"), "w", encoding="utf-8") as tempFile:
            tempFile.write(code)
            tempFile.close()

        commandALIF = os.path.join(fileDir, "temp.alif")
        if os.path.exists("Temp/temp.exe"):
            os.remove("Temp/temp.exe")
            res = os.system("alif " + commandALIF)
        else:
            res = os.system("alif " + commandALIF)

        if res == 0:
            if sys.platform == "linux":
                process = subprocess.Popen(["./temp"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       universal_newlines=True, encoding="utf-8", cwd=fileDir)
            else:
                process = subprocess.Popen(["temp.exe"], shell=True, stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           universal_newlines=True, encoding="utf-8", cwd=fileDir)
            # rc = process.wait()
            out, err = process.communicate()
            process_time = round(time.time() - start_time, 5)
            self.result.setText(f"{out}\n{err}\n\n [انتهى التنفيذ خلال: {process_time} ثانية]\n")
        else:
            try:
                log = os.path.join(fileDir, "temp.alif.log")
                log_open = open(log, "r", encoding="utf-8")
                self.result.setText(log_open.read())
                log_open.close()
            except:
                self.result.setText("تحقق من أن لغة ألف 3 مثبتة بشكل صحيح")

    def retranslateUi(self, MainWin):
        _translate = QCoreApplication.translate
        MainWin.setWindowTitle(_translate("MainWin", "MainWindow"))
        self.title.setText(_translate("MainWin", "طيف"))
        self.statusLable.setText(_translate("MainWin", "بيئة تطوير لغة ألف 3 - نسخة 0.2.2"))
        self.newBtn.setToolTip("جديد")
        self.openBtn.setToolTip("فتح")
        self.saveBtn.setToolTip("حفظ")
        self.runBtn.setToolTip("تشغيل")


#######################################################################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWin = QMainWindow()
    ui = Ui_MainWin()
    ui.setupUi(MainWin)
    MainWin.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    MainWin.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    MainWin.show()
    sys.exit(app.exec())
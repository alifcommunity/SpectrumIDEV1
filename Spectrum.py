from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QFrame, QApplication, QSizeGrip, QFileDialog, QPlainTextEdit
from PyQt6.QtCore import QSize, Qt, QPointF, QProcess
from PyQt6.QtGui import QIcon, QPixmap, QTextCursor
from tempfile import gettempdir
from PyQt6 import sip
import CodeEditor
import time
import sys
import os

################################################## تعريف الواجهة الرئيسية ##############################################

class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1280, 720)
        self.setMinimumSize(QSize(640, 360))
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.vMainWinLay = QVBoxLayout(self)
        self.vMainWinLay.setContentsMargins(0, 0, 0, 0)
        self.vMainWinLay.setSpacing(0)

        self.mainWid = QWidget(self)
        self.mainWid.setStyleSheet("background-color:#1c1d20; border-radius: 7px")

        self.vMainWidLay = QVBoxLayout(self.mainWid)
        self.vMainWidLay.setContentsMargins(0, 0, 0, 0)
        self.vMainWidLay.setSpacing(0)

        self.topBarFrm = QFrame(self.mainWid)
        self.topBarFrm.setStyleSheet("background-color: #1c1d20;")
        self.topBarFrm.setFixedHeight(45)
        self.topBarFrm.mousePressEvent = self.mousePress
        self.topBarFrm.mouseMoveEvent = self.mouseMove
        self.topBarFrm.mouseReleaseEvent = self.mouseRelese

        self.hTopBarFrmLay = QHBoxLayout(self.topBarFrm)
        self.hTopBarFrmLay.setContentsMargins(3, 0, 3, 0)
        self.hTopBarFrmLay.setSpacing(0)

        self.logoFrm = QFrame(self.topBarFrm)
        self.logoFrm.setFixedWidth(90)

        self.hLogoFrmLay = QHBoxLayout(self.logoFrm)
        self.hLogoFrmLay.setContentsMargins(43, 1, 0, 0)
        self.hLogoFrmLay.setSpacing(0)

        self.alifBtn = QPushButton(self.logoFrm)
        self.alifBtn.setFixedHeight(40)
        self.alifBtn.setFixedWidth(40)
        self.alifBtn.setStyleSheet("background-color: #1c1d20;border: 0px")
        self.alifBtn.setIcon(QIcon("./icons/TaifLogo.svg"))
        self.alifBtn.setIconSize(QSize(30, 30))

        self.hLogoFrmLay.addWidget(self.alifBtn)
        self.hTopBarFrmLay.addWidget(self.logoFrm)

        self.titleFrm = QFrame(self.topBarFrm)

        self.hTitleFrmLay = QHBoxLayout(self.titleFrm)
        self.hTitleFrmLay.setContentsMargins(0, 0, 0, 0)
        self.hTitleFrmLay.setSpacing(0)

        self.title = QLabel(self.titleFrm)
        self.title.setText("جمع.alif")
        self.title.setStyleSheet("font: 12pt Tajawal; color:#fff;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hTitleFrmLay.addWidget(self.title)
        self.hTopBarFrmLay.addWidget(self.titleFrm)

        self.controlWinFrm = QFrame(self.topBarFrm)
        self.controlWinFrm.setFixedWidth(90)

        self.hControlWinFrmLay = QHBoxLayout(self.controlWinFrm)
        self.hControlWinFrmLay.setContentsMargins(0, 0, 0, 0)
        self.hControlWinFrmLay.setSpacing(0)

        self.minimizeBtn = QPushButton(self.controlWinFrm)
        self.minimizeBtn.setStyleSheet("QPushButton{background-color: #1c1d20; border-radius: 3px;}QPushButton:hover{background-color: #4955FF;}QPushButton:pressed{background-color: #323AAF;}")
        self.minimizeBtn.setFixedHeight(25)
        self.minimizeBtn.setFixedWidth(25)
        self.minimizeBtn.setIcon(QIcon("./icons/Minimize.svg"))
        self.minimizeBtn.setIconSize(QSize(13, 13))
        self.minimizeBtn.clicked.connect(self.showMinimized)

        self.hControlWinFrmLay.addWidget(self.minimizeBtn)

        self.maximizeBtn = QPushButton(self.controlWinFrm)
        self.maximizeBtn.setStyleSheet("QPushButton{background-color: #1c1d20; border-radius: 3px;}QPushButton:hover{background-color: #4955FF;}QPushButton:pressed{background-color: #323AAF;}")
        self.maximizeBtn.setFixedWidth(25)
        self.maximizeBtn.setFixedHeight(25)
        self.maximizeBtn.setIcon(QIcon("./icons/Maximize.svg"))
        self.maximizeBtn.setIconSize(QSize(13, 13))
        self.maximizeBtn.clicked.connect(self.winRestore)

        self.hControlWinFrmLay.addWidget(self.maximizeBtn)

        self.closeBtn = QPushButton(self.controlWinFrm)
        self.closeBtn.setStyleSheet("QPushButton{background-color: #1c1d20; border-radius: 3px;}QPushButton:hover{background-color: #DA0000;}QPushButton:pressed{background-color: #323AAF;}")
        self.closeBtn.setFixedHeight(25)
        self.closeBtn.setFixedWidth(25)
        self.closeBtn.setIcon(QIcon("./icons/Close.svg"))
        self.closeBtn.setIconSize(QSize(13, 13))
        self.closeBtn.clicked.connect(self.close)

        self.hControlWinFrmLay.addWidget(self.closeBtn)
        self.hTopBarFrmLay.addWidget(self.controlWinFrm)
        self.vMainWidLay.addWidget(self.topBarFrm)

        self.mainFrm = QFrame(self.mainWid)
        self.mainFrm.setStyleSheet("background-color: #1c1d20;")

        self.hMainFrmLay = QHBoxLayout(self.mainFrm)
        self.hMainFrmLay.setContentsMargins(0, 0, 0, 0)
        self.hMainFrmLay.setSpacing(0)

        self.menuFrm = QFrame(self.mainFrm)
        self.menuFrm.setStyleSheet("background-color: #1c1d20;")
        self.menuFrm.setFixedWidth(50)
        self.menuFrm.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.vMenuFrmLay = QVBoxLayout(self.menuFrm)
        self.vMenuFrmLay.setContentsMargins(0, 3, 0, 0)
        self.vMenuFrmLay.setSpacing(0)

        self.topBtnsFrm = QFrame(self.menuFrm)

        self.vTopBtnsFrmLay = QVBoxLayout(self.topBtnsFrm)
        self.vTopBtnsFrmLay.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vTopBtnsFrmLay.setContentsMargins(0, 0, 5, 0)
        self.vTopBtnsFrmLay.setSpacing(6)

        self.newBtn = QPushButton(self.topBtnsFrm)
        self.newBtn.setToolTip("جديد")
        self.newBtn.setStyleSheet("QPushButton{background-color: #1c1d20; color: #fff; border-radius: 7px;}QPushButton:hover{background-color: #4955FF;}QPushButton:pressed{background-color: #323AAF;}")
        self.newBtn.setFixedWidth(40)
        self.newBtn.setFixedHeight(40)
        self.newBtn.setIcon(QIcon("./icons/New.svg"))
        self.newBtn.setIconSize(QSize(25, 25))
        self.newBtn.clicked.connect(self.newFile)

        self.vTopBtnsFrmLay.addWidget(self.newBtn)

        self.openBtn = QPushButton(self.topBtnsFrm)
        self.openBtn.setToolTip("فتح")
        self.openBtn.setStyleSheet("QPushButton{background-color: #1c1d20; color: #fff; border-radius: 7px;}QPushButton:hover{background-color: #4955FF;}QPushButton:pressed{background-color: #323AAF;}")
        self.openBtn.setFixedWidth(40)
        self.openBtn.setFixedHeight(40)
        self.openBtn.setIcon(QIcon("./icons/Open.svg"))
        self.openBtn.setIconSize(QSize(25, 25))
        self.openBtn.clicked.connect(self.openFile)

        self.vTopBtnsFrmLay.addWidget(self.openBtn)

        self.saveBtn = QPushButton(self.topBtnsFrm)
        self.saveBtn.setToolTip("حفظ")
        self.saveBtn.setStyleSheet("QPushButton{background-color: #1c1d20; color: rgb(255, 255, 255); border-radius: 7px;}QPushButton:hover{background-color: #4955FF;}QPushButton:pressed{background-color: #323AAF;}")
        self.saveBtn.setFixedHeight(40)
        self.saveBtn.setFixedWidth(40)
        self.saveBtn.setIcon(QIcon("./icons/Save.svg"))
        self.saveBtn.setIconSize(QSize(25, 25))
        self.saveBtn.clicked.connect(self.saveFile)

        self.vTopBtnsFrmLay.addWidget(self.saveBtn)

        self.saveAsBtn = QPushButton(self.topBtnsFrm)
        self.saveAsBtn.setToolTip("حفظ كـ")
        self.saveAsBtn.setStyleSheet("QPushButton{background-color: #1c1d20; color: rgb(255, 255, 255); border-radius: 7px;}QPushButton:hover{background-color: #4955FF;}QPushButton:pressed{background-color: #323AAF;}")
        self.saveAsBtn.setFixedHeight(40)
        self.saveAsBtn.setFixedWidth(40)
        self.saveAsBtn.setIcon(QIcon("./icons/SaveAs.svg"))
        self.saveAsBtn.setIconSize(QSize(25, 25))
        self.saveAsBtn.clicked.connect(self.saveFileAs)

        self.vTopBtnsFrmLay.addWidget(self.saveAsBtn)
        self.vMenuFrmLay.addWidget(self.topBtnsFrm)

        self.runBtnFrm = QFrame(self.menuFrm)

        self.vRunBtnFrmLay = QVBoxLayout(self.runBtnFrm)
        self.vRunBtnFrmLay.setContentsMargins(0, 0, 5, 7)
        self.vRunBtnFrmLay.setSpacing(6)

        self.buildBtn = QPushButton(self.runBtnFrm)
        self.buildBtn.setToolTip("بناء")
        self.buildBtn.setStyleSheet("QPushButton{background-color: #1c1d20; color: rgb(255, 255, 255); border-radius: 7px;}QPushButton:hover{background-color: #FF5733;}QPushButton:pressed{background-color: #323AAF;}")
        self.buildBtn.setFixedWidth(40)
        self.buildBtn.setFixedHeight(40)
        self.buildBtn.setIcon(QIcon("./icons/Build.svg"))
        self.buildBtn.setIconSize(QSize(25, 25))
        self.buildBtn.clicked.connect(self.codeBuild)

        self.runBtn = QPushButton(self.runBtnFrm)
        self.runBtn.setToolTip("تشغيل")
        self.runBtn.setStyleSheet("QPushButton{background-color: #1c1d20; color: rgb(255, 255, 255); border-radius: 7px;}QPushButton:hover{background-color: #F6FF43;}QPushButton:pressed{background-color: #DFE300;}")
        self.runBtn.setFixedWidth(40)
        self.runBtn.setFixedHeight(40)
        self.runBtn.setIcon(QIcon("./icons/Run.svg"))
        self.runBtn.setIconSize(QSize(25, 25))
        self.runBtn.clicked.connect(self.runCode)

        self.vRunBtnFrmLay.addWidget(self.buildBtn)
        self.vRunBtnFrmLay.addWidget(self.runBtn)
        self.vRunBtnFrmLay.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.vMenuFrmLay.addWidget(self.runBtnFrm)
        self.hMainFrmLay.addWidget(self.menuFrm)

        self.codeFrm = QFrame(self.mainFrm)

        self.vCodeFrmLay = QVBoxLayout(self.codeFrm)
        self.vCodeFrmLay.setContentsMargins(6, 0, 0, 6)

        self.code = CodeEditor.CodeEditor(self.codeFrm)

        self.vCodeFrmLay.addWidget(self.code)

        self.result = QPlainTextEdit(self.codeFrm)
        self.result.setStyleSheet("background-color: #0A0B0C; color: #fff; font: 11pt Tajawal; border-radius: 7px;")
        self.resOpt = self.result.document().defaultTextOption()
        self.resOpt.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.resOpt.setTextDirection(Qt.LayoutDirection.RightToLeft)
        self.result.document().setDefaultTextOption(self.resOpt)
        self.result.setReadOnly(True)
        self.result.setFixedHeight(210)
        self.result.appendPlainText(os.getcwd())
        self.result.keyPressEvent = self.resutlReturn

        self.vCodeFrmLay.addWidget(self.result)

        self.statusBar = QFrame(self.mainWid)
        self.statusBar.setStyleSheet("background-color: #1c1d20; border-radius: 9px;")
        self.statusBar.setFixedHeight(25)

        self.hStatusLay = QHBoxLayout(self.statusBar)
        self.hStatusLay.setContentsMargins(6, 0, 0, 0)

        self.statusLable = QLabel(self.statusBar)
        self.statusLable.setText("بيئة تطوير لغة ألف 3 - نسخة 0.3.0")
        self.statusLable.setStyleSheet("color: rgb(190, 190, 190); font: 9pt Tajawal")
        self.statusLable.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.hStatusLay.addWidget(self.statusLable)

        self.resizeGrip = QSizeGrip(self.statusBar)
        self.resizeGrip.setFixedWidth(15)
        self.resizeGrip.setFixedHeight(15)
        self.resizeLable = QLabel(self.resizeGrip)
        self.resizeLable.setPixmap(QPixmap("./icons/Resize.svg"))

        QFileDialog.setWindowIcon(self, QIcon("./icons/Alif.ico"))

        self.hStatusLay.addWidget(self.resizeGrip)
        self.hMainFrmLay.addWidget(self.codeFrm)
        self.vMainWidLay.addWidget(self.mainFrm)
        self.vMainWidLay.addWidget(self.statusBar)
        self.vMainWinLay.addWidget(self.mainWid)
        self.setCentralWidget(self.mainWid)

#################################################### تعريف المتغيرات ###################################################

        self.fileOpened = False
        self.fileSaved = False
        self.fileName = None
        self.processRuned = False
        self.res = 1

################################################ تعريف الوظائف الرئيسية ################################################

    def winRestore(self):
        if self.isMaximized():
            self.mainWid.setStyleSheet("background-color: #1c1d20; border-radius: 10px")
            self.maximizeBtn.setIcon(QIcon("./icons/Maximize.svg"))
            self.showNormal()
        else:
            self.maximizeBtn.setIcon(QIcon("./icons/Restore.svg"))
            self.mainWid.setStyleSheet("background-color: #1c1d20")
            self.showMaximized()

    def mousePress(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressedFlag = True
            self.oldPos = event.globalPosition()

    def mouseMove(self, event):
        if self.pressedFlag:
            if self.isMaximized():
                self.maximizeBtn.setIcon(QIcon("./icons/Maximize.svg"))
                self.mainWid.setStyleSheet("background-color: #1c1d20; border-radius: 10px")
                self.showNormal()
                self.oldPos = QPointF(self.pos()) + QPointF(640.0, 25.0)
            delta = QPointF.toPoint(event.globalPosition() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition()

    def mouseRelese(self, event):
        self.pressedFlag = False

    def isSaved(self):
        if self.code.document().isModified() or self.fileName == None:
            self.saveFile()
        return True

    def newFile(self):
        if self.isSaved():
            self.code.clear()
            self.result.clear()
            self.fileOpened = False
            self.fileSaved = False
            self.fileName = None
            self.title.setText("غير معنون.alif")

    def saveFile(self):
        code = self.code.toPlainText()
        if self.fileOpened:
            if self.fileName:
                with open(self.fileName, "w", encoding="utf-8") as saveFile:
                    saveFile.write(code)
                    saveFile.close()
        elif self.fileSaved:
            if self.fileName:
                with open(self.fileName, "w", encoding="utf-8") as saveFile:
                    saveFile.write(code)
                    saveFile.close()
        else:
            self.fileName, _ = QFileDialog.getSaveFileName(self, "حفظ ملف ألف", "غير معنون.alif", "ملف ألف (*.alif)")
            if self.fileName:
                with open(self.fileName, "w", encoding="utf-8") as saveFile:
                    saveFile.write(code)
                    saveFile.close()
                self.setWinTitle()
                self.fileSaved = True
            else:
                self.fileName = None

    def saveFileAs(self):
        code = self.code.toPlainText()
        self.fileName, _ = QFileDialog.getSaveFileName(self, "حفظ ملف ألف", "غير معنون.alif", "ملف ألف (*.alif) ;; كل الملفات (*)")
        if self.fileName:
            with open(self.fileName, "w", encoding="utf-8") as saveFileAs:
                saveFileAs.write(code)
                saveFileAs.close()
            self.setWinTitle()
        else:
            self.fileName = None

    def openFile(self):
        if self.isSaved():
            self.fileName, _ = QFileDialog.getOpenFileName(self, "فتح ملف ألف", "", "كل الملفات (*.alif)")
            if self.fileName:
                with open(self.fileName, "r", encoding="utf-8") as openFile:
                    fileCode = openFile.read()
                    self.code.setPlainText(fileCode)
                    openFile.close()
                self.setWinTitle()
                self.fileOpened = True
            else:
                self.fileName = None

    def codeBuild(self):
        self.startTime = time.time()
        code = self.code.toPlainText()
        self.tempFile = gettempdir()

        with open(os.path.join(self.tempFile, "temp.alif"), "w", encoding="utf-8") as temporaryFile:
            temporaryFile.write(code)
            temporaryFile.close()

        alifCom = os.path.join(self.tempFile, "temp.alif")
        self.res = QProcess.execute("alif ", [alifCom])

        buildTime = round(time.time() - self.startTime, 3)
        self.result.appendPlainText(f"[انتهى البناء خلال: {buildTime} ثانية]")

        if self.res == 1:
            try:
                log = os.path.join(self.tempFile, "temp.alif.log")
                log_open = open(log, "r", encoding="utf-8")
                self.result.setPlainText(log_open.read())
                log_open.close()
            except:
                self.result.setPlainText("تحقق من أن لغة ألف 3 مثبتة بشكل صحيح")

    def runCode(self):
        self.startTime = time.time()
        if self.res == 0:
            if sys.platform == "linux":
                self.process = QProcess()
                self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
                self.process.readyRead.connect(self.ifReadReady)
                self.process.start(os.path.join(self.tempFile, "./temp"))
            else:
                self.process = QProcess()
                self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
                self.process.readyRead.connect(self.ifReadReady)
                self.process.start(os.path.join(self.tempFile, "temp.exe"))
            self.processRuned = True
        else:
            self.result.setPlainText("قم ببناء الشفرة أولاً")

    def ifReadReady(self):
        self.result.setReadOnly(False)
        self.result.appendPlainText(str(self.process.readAll(), "utf-8"))
        runTime = round(time.time() - self.startTime, 3)
        self.result.appendPlainText(f"\n[انتهى التنفيذ خلال: {runTime} ثانية]")

    def resutlReturn(self, event):
        self.cursor = self.result.textCursor()
        self.cursor.movePosition(QTextCursor.MoveOperation.StartOfLine)
        self.cursor.movePosition(QTextCursor.MoveOperation.EndOfLine, QTextCursor.MoveMode.KeepAnchor)
        self.input = self.cursor.selectedText() + "\n"
        if event.key() == Qt.Key.Key_Return:
            if self.processRuned:
                self.process.write(self.input.encode())
            print(self.input)
        QPlainTextEdit.keyPressEvent(self.result, event)

    def setWinTitle(self):
        self.title.setText(self.fileName.split("/")[-1])

################################################## دالة تشغيل التطبيق ##################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWin()
    mainWin.setWindowFlags(Qt.WindowType.FramelessWindowHint)
    mainWin.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    mainWin.show()
    sys.exit(app.exec())

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qsci import *
from gui.Lexer import Lexer
from gui.output_Lexer import output_Lexer
from gui.debug_Lexer import debug_Lexer
from assembler.Asm import asm
from disassembler.DisAsm import disasm
import re
import os
import struct
from gui.resource import *
class ScintillaEditor(QMainWindow):
        """docstring for Scintilla"""
        def __init__(self,parent=None):
            super().__init__(parent)
            w = QDesktopWidget()
            self.rect = w.screenGeometry()
            self.setupUI()

            self.scintilla.linesChanged.connect(self.linesChanged)
            self.output.linesChanged.connect(self.linesChanged)
            self.debug.linesChanged.connect(self.linesChanged)
            self.scintilla.textChanged.connect(self.textchanged)

        def linesChanged(self):
            self.scintilla.setMarginWidth(0, self.fontmetrics.width(str(self.scintilla.lines())) + 5)
            self.output.setMarginWidth(0, self.fontmetrics.width(str(self.output.lines())) + 5)
            self.debug.setMarginWidth(0, self.fontmetrics.width(str(self.debug.lines())) + 5)

        def textchanged(self):
            if self.unsaved != True:
                self.unsaved = True
                self.label.setText(self.label.text() + '*')

        def dragEnterEvent(self, a0: QDragEnterEvent):
            if a0.mimeData().hasText() or a0.mimeData().hasUrls:
                a0.accept()
            else:
                a0.ignore()

        def dropEvent(self, a0: QDropEvent):
            fname = a0.mimeData().urls()[0].path()
            if(not fname):
                return
            try:
                with open(fname, 'r+') as f:
                    self.scintilla.setText(f.read())
                self.current_path, self.current_filename = os.path.split(fname)
                self.label.setText(self.current_filename)
                self.unsaved = False
                self.output.append('Open file : ' + fname+'\n')
            except Exception as e:
                self.output.append('Output : Can\'t open this file.\n')

        def closeEvent(self, a0: QCloseEvent):
            if(self.unsaved):
                answer = QMessageBox.question(self, 'Attention!',
                        'The open file is unsaved, are you sure to exit?', QMessageBox.Yes|QMessageBox.No)
                if answer == QMessageBox.Yes:
                    self.writesettings()
                    a0.accept()
                else:
                    a0.ignore()

        def writesettings(self):
            self.settings = QSettings("LINC corporation", "MIPS Editor")
            self.settings.beginGroup('ScintillaEditor')
            self.settings.setValue('font',self.font)
            self.settings.setValue('color', self.color)
            self.settings.sync()
            self.settings.endGroup()

        def readsettings(self):
            self.settings = QSettings("LINC corporation", "MIPS Editor")
            self.settings.beginGroup('ScintillaEditor')
            self.font = self.settings.value('font',self.font)
            self.color = self.settings.value('color', self.color)
            self.settings.endGroup()

        @pyqtSlot()
        def on_actionRestore_triggered(self):
            self.font.setFamily("Microsoft YaHei UI")
            #self.font.setPointSize(17)
            self.font.setFixedPitch(True)
            self.fontmetrics = QFontMetrics(self.font)
            font_name = QFontDatabase.addApplicationFont(":/resource/ASM/resource/SourceCodePro-Regular.ttf")
            if (font_name != -1):
                self.font.setFamily('Source Code Pro')
            self.setFont(self.font)
            self.color = QColor("#00ff00")
            self.output_lexer.setColor(self.color,0)
            self.debug_lexer.setColor(self.color, 0)
            self.scintilla.setFont(self.font)
            self.fontmetrics = QFontMetrics(self.font)
            self.lexer.setFont(self.font)
            self.label.setFont(self.font)
            self.debug_label.setFont(self.font)
            self.scintilla.setMarginsFont(self.font)
            self.output_lexer.setFont(self.font)
            self.output.setMarginsFont(self.font)
            self.output.setIndentationWidth(int(self.font.pointSize() / 3))
            self.output.setTabWidth(4)
            self.output.setMarginWidth(0, self.fontmetrics.width(str(self.output.lines())) + 5)
            self.debug_lexer.setFont(self.font)
            self.debug.setMarginsFont(self.font)
            self.debug.setIndentationWidth(int(self.font.pointSize() / 3))
            self.debug.setTabWidth(4)
            self.debug.setMarginWidth(0, self.fontmetrics.width(str(self.debug.lines())) + 5)
            self.scintilla.setIndentationWidth(int(self.font.pointSize()))
            self.scintilla.setAutoIndent(True)
            self.scintilla.setTabWidth(4)
            self.scintilla.setMarginWidth(0, self.fontmetrics.width(str(self.scintilla.lines())) + 5)
            self.output.append('Default settings successfully restored.\n')

        @pyqtSlot()
        def on_actionOpen_triggered(self):
            fname, _ = QFileDialog.getOpenFileName(self, 'Open file',
                    filter="ASM Files (*.asm *.s);;Text Files (*.txt);;All Files (*.*)")
            try:
                with open(fname,'r+', encoding="UTF8") as f:
                    self.scintilla.setText(f.read())
                self.current_path,self.current_filename = os.path.split(fname)
                self.label.setText(self.current_filename)
            except Exception as e:
                self.output.append('Output : Can\'t open this file.\n')
            self.unsaved = False

        @pyqtSlot()
        def on_actionNew_triggered(self):
            if (self.unsaved):
                answer = QMessageBox.question(self, 'Attention!',
                                              'The open file is unsaved, are '
                                              'you sure to open another file?',
                                              QMessageBox.Yes | QMessageBox.No)
                if answer == QMessageBox.No:
                    return
            fname = 'untitled.s'
            self.current_filename = fname
            self.label.setText(fname)
            self.scintilla.setText('')
            self.unsaved = False

        @pyqtSlot()
        def on_actionSave_triggered(self):
            if(self.current_filename != 'untitled.s'):
                with open(os.path.join(self.current_path,self.current_filename),'w+') as f:
                    f.write(self.scintilla.text())
                self.output.append('Output : Successfully saved file at'
                                   + os.path.join(self.current_path,self.current_filename) +'\n')
            else:
                fname , _= QFileDialog.getSaveFileName(self, 'Save file',
                    filter="ASM Files (*.asm *.s);;Text Files (*.txt);;All Files (*.*)")
                if fname:
                    with open(fname,'w+') as f:
                        f.write(self.scintilla.text())
                    _, self.current_filename = os.path.split(fname)
                    self.label.setText(self.current_filename)
                    self.output.append('Output : Successfully saved file at'
                                       + os.path.join(self.current_path,self.current_filename) + '\n')

        @pyqtSlot()
        def on_actionSave_As_triggered(self):
            fname, _ = QFileDialog.getSaveFileName(self, 'Save file',
                filter="ASM Files (*.asm *.s);;Text Files (*.txt);;All Files (*.*)")
            if fname:
                with open(fname, 'w+') as f:
                    f.write(self.scintilla.text())
                self.current_path, self.current_filename = os.path.split(fname)
                self.label.setText(self.current_filename)
                self.output.append('Output : Successfully saved file at'
                                   + os.path.join(self.current_path,self.current_filename) + '\n')
        @pyqtSlot()
        def on_actionPrint_triggered(self):
            pass
        @pyqtSlot()
        def on_actionExit_triggered(self):
            self.close()
        @pyqtSlot()
        def on_actionCut_triggered(self):
            self.scintilla.cut()
        @pyqtSlot()
        def on_actionCopy_triggered(self):
            self.scintilla.copy()
        @pyqtSlot()
        def on_actionPaste_triggered(self):
            self.scintilla.paste()
        @pyqtSlot()
        def on_actionDelete_triggered(self):
            self.scintilla.removeSelectedText()
        @pyqtSlot()
        def on_actionFind_triggered(self):
            text, ok = QInputDialog.getText(self, 'Input Dialog','Enter the search text:')
            if ok:
                self.scintilla.findFirst(text,0,0,0,0)
        @pyqtSlot()
        def on_actionSelect_All_triggered(self):
            self.scintilla.selectAll()
        @pyqtSlot()
        def on_actionUndo_triggered(self):
            self.scintilla.undo()
        @pyqtSlot()
        def on_actionRedo_triggered(self):
            self.scintilla.redo()
        @pyqtSlot()
        def on_actionGenerate_bin_triggered(self):
            fname, _ = QFileDialog.getSaveFileName(self, 'Save bin file',
                    filter="bin Files (*.bin);;Text Files (*.txt);;All Files (*.*)")
            if not fname:
                return
            text = self.scintilla.text()
            result, line, e, process = asm(text)
            if line == -1:
                with open(fname,'wb') as f:
                    f.write(int(result,2).to_bytes(int(len(result)/8), byteorder='big'))
                self.output.append('Output : Successfully generated bin file.\n')
            else:
                if (re.search('Line', str(e))):
                    if (process == 1):
                        self.output.append('(During First Scan)' + str(e)+'\n')
                    if (process == 2):
                        self.output.append('(During Second Scan)' + str(e)+'\n')
                else:
                    if (process == 1):
                        self.output.append('(During First Scan:Unexpected ERROR!)'
                                           + 'Line %d :' % line + str(e)+'\n')
                    if (process == 2):
                        self.output.append('(During Second Scan:Unexpected ERROR!)'
                                           + 'Line %d :' % line + str(e)+'\n')

        @pyqtSlot()
        def on_actionGenerate_coe_triggered(self):
            fname, _ = QFileDialog.getSaveFileName(self, 'Save bin file',
                    filter="coe Files (*.coe);;Text Files (*.txt);;All Files (*.*)")
            if not fname:
                return
            text = self.scintilla.text()
            result, line, e, process = asm(text)
            if line == -1:
                with open(fname,'w+') as f:
                    f.write('memory_initialization_radix=16;\nmemory_initialization_vector=\n')
                    i = 0
                    while i < len(result)-32:
                        temp = hex(int(result[i:i+32], 2))[2:].upper()
                        while len(temp) < 8:
                            temp = '0' + temp
                        f.write(temp)
                        f.write(',')
                        i = i + 32
                        if(i % (32*4) == 0):
                            f.write('\n')
                    temp = hex(int(result[len(result)-32:len(result)], 2))[2:].upper()
                    while len(temp) < 8:
                        temp = '0' + temp
                    f.write(temp)
                    f.write(';')
                self.output.append('Output : Successfully generated coe file.\n')
            else:
                if (re.search('Line', str(e))):
                    if (process == 1):
                        self.output.append('(During First Scan)' + str(e)+'\n')
                    if (process == 2):
                        self.output.append('(During Second Scan)' + str(e)+'\n')
                else:
                    if (process == 1):
                        self.output.append('(During First Scan:Unexpected ERROR!\n)'
                                           + 'Line %d :' % line + str(e)+'\n')
                    if (process == 2):
                        self.output.append('(During Second Scan:Unexpected ERROR!\n)'
                                           + 'Line %d :' % line + str(e)+'\n')

        @pyqtSlot()
        def on_actionDebug_File_triggered(self):
            self.debug.setText('')
            text = self.scintilla.text()
            result,line,e,process = asm(text)
            if line == -1:
                i = 0
                while i < len(result):
                    self.debug.append(hex(int((i + 32) / 32)) + ' : ' + result[i:i + 32] + '\n')
                    i = i + 32
                self.debug_label.setText('Debug Console (bin)')
                self.output.append('Output : Successfully generated debug(bin) file.\n')
            else:
                if(re.search('Line',str(e))):
                    if(process == 1):
                        self.output.append('(During First Scan)'+ str(e)+'\n')
                    if(process == 2):
                        self.output.append('(During Second Scan)' + str(e)+'\n')
                else:
                    if (process == 1):
                        self.output.append('(During First Scan:Unexpected ERROR!)\n'
                                           + 'Line %d :' % line + str(e)+'\n')
                    if (process == 2):
                        self.output.append('(During Second Scan:Unexpected ERROR!)\n'
                                           + 'Line %d :' % line + str(e)+'\n')

        @pyqtSlot()
        def on_actionDebug_File_hex_triggered(self):
            self.debug.setText('')
            text = self.scintilla.text()
            result, line, e, process = asm(text)
            if line == -1:
                i = 0
                while i < len(result):
                    self.debug.append(hex(int((i + 32) / 32)) + ' : ' +
                    hex(int(result[i:i + 32],2)).replace('0x','').upper().zfill(8) + '\n')
                    i = i + 32
                self.debug_label.setText('Debug Console (hex)')
                self.output.append('Output : Successfully generated debug(hex) file.\n')
            else:
                if (re.search('Line', str(e))):
                    if (process == 1):
                        self.output.append('(During First Scan)' + str(e) + '\n')
                    if (process == 2):
                        self.output.append('(During Second Scan)' + str(e) + '\n')
                else:
                    if (process == 1):
                        self.output.append('(During First Scan:Unexpected ERROR!)\n'
                                           + 'Line %d :' % line + str(e) + '\n')
                    if (process == 2):
                        self.output.append('(During Second Scan:Unexpected ERROR!)\n'
                                           + 'Line %d :' % line + str(e) + '\n')

        @pyqtSlot()
        def on_actionLoad_bin_triggered(self):
            fname, _ = QFileDialog.getOpenFileName(self, 'Open bin file',
                                                   filter="bin Files (*.bin);;All Files (*.*)")
            try:
                with open(fname, 'rb') as f:
                    tmp = f.read(4)
                    lists = []
                    while tmp:
                        if len(tmp) != 4:
                            raise Exception('bin file %s \'s length is not a multiple of four.\n' % fname)
                        lists.append(bin(struct.unpack('>i', bytes(tmp))[0])[2:].zfill(32))
                        tmp = f.read(4)
                    text, e = disasm(lists)
                    if e != 0:
                        raise e
                    self.scintilla.setText(text)
                    self.unsaved = False
                    self.output.append('Output : Successfully disassembled bin file.\n')
            except Exception as e:
                self.output.append(str(e) + '\n')

        @pyqtSlot()
        def on_actionLoad_coe_triggered(self):
            fname, _ = QFileDialog.getOpenFileName(self, 'Open coe file',
                                                   filter="coe Files (*.coe);;All Files (*.*)")
            try:
                with open(fname, 'r+') as f:
                    f.read(62)
                    txt = f.read()
                    lists = txt.split(',')
                    lists = [i.replace('\n', '') for i in lists]
                    lists = [i.replace(';', '') for i in lists]
                    lists = [bin(int(i, 16))[2:].zfill(32) for i in lists]
                    text, e = disasm(lists)
                    if e != 0:
                        raise e
                    self.scintilla.setText(text)
                    self.unsaved = False
                    self.output.append('Output : Successfully disassembled coe file.\n')
            except Exception as e:
                self.output.append(str(e) + '\n')

        @pyqtSlot()
        def on_actionColor_triggered(self):
            print('he')
            self.color = QColorDialog.getColor()
            if self.color.isValid():
                self.output_lexer.setColor(self.color, 0)
                self.debug_lexer.setColor(self.color, 0)

        @pyqtSlot()
        def on_actionResize_triggered(self):
            self.font, ok = QFontDialog.getFont()
            if ok:
                self.scintilla.setFont(self.font)
                self.fontmetrics = QFontMetrics(self.font)
                self.lexer.setFont(self.font)
                self.label.setFont(self.font)
                self.debug_label.setFont(self.font)
                self.scintilla.setMarginsFont(self.font)
                self.output_lexer.setFont(self.font)
                self.output.setMarginsFont(self.font)
                self.output.setIndentationWidth(int(self.font.pointSize() / 3))
                self.output.setTabWidth(4)
                self.output.setMarginWidth(0, self.fontmetrics.width(str(self.output.lines())) + 5)
                self.debug_lexer.setFont(self.font)
                self.debug.setMarginsFont(self.font)
                self.debug.setIndentationWidth(int(self.font.pointSize() / 3))
                self.debug.setTabWidth(4)
                self.debug.setMarginWidth(0, self.fontmetrics.width(str(self.debug.lines())) + 5)
                self.scintilla.setIndentationWidth(int(self.font.pointSize() / 3))
                self.scintilla.setTabWidth(4)
                self.scintilla.setMarginWidth(0, self.fontmetrics.width(str(self.scintilla.lines())) + 5)

        @pyqtSlot()
        def on_actionFull_triggered(self):
            self.showFullScreen()
        @pyqtSlot()
        def on_actionNormalWindow_triggered(self):
            self.showNormal()
        @pyqtSlot()
        def on_actionMinimize_triggered(self):
            self.showMinimized()
        @pyqtSlot()
        def on_actionMaximize_triggered(self):
            self.showMaximized()
        @pyqtSlot()
        def on_actionAbout_triggered(self):
            message = QDialog(self)
            message.setWindowTitle('About')
            photo = QPixmap(':/resource/ASM/resource/about.jpg')
            photo = photo.scaled(int(photo.width()/1.5),int(photo.height()/1.5),Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            message.setFixedSize(photo.width(),photo.height())
            message.label = QLabel(message)
            message.label.setPixmap(photo)
            message.show()


        def setupUI(self):
            #self.setUnifiedTitleAndToolBarOnMac(True)
            self.setWindowTitle("MiniASM")
            self.setMinimumSize(int(self.rect.width()/2.5),int(self.rect.height()/2.5))
            self.setBaseSize(int(self.rect.width()/1.5),int(self.rect.height()/1.5))
            self.__menubar__()
            self.title = '*MIPS ASM'
            self.unsaved = False
            self.out_of_loop = False
            self.current_filename = 'untitled.s'
            self.current_path = ''
            self.color = QColor("#00ff00")
            self.setAcceptDrops(True)
            self.label = QLabel(self.title)
            self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.label.setBaseSize(int(self.rect.width()/2.7),10)
            self.debug_label = QLabel('Debug Console')
            self.debug_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.debug_label.setBaseSize(int(self.rect.width() / 6), 10)

            self.textbrowser = QTextBrowser()

            self.font = QFont()
            self.font.setFamily("Microsoft YaHei UI")
            #self.font.setPointSize(int(self.rect.width()/90))
            self.font.setFixedPitch(True)
            self.fontmetrics = QFontMetrics(self.font)
            font_name = QFontDatabase.addApplicationFont(":/resource/ASM/resource/SourceCodePro-Regular.ttf")
            if (font_name != -1):
                self.font.setFamily('Source Code Pro')
            self.setFont(self.font)
            self.readsettings()
            self.layout = QVBoxLayout()
            self.layout.setAlignment(Qt.AlignVCenter)
            self.layout.setContentsMargins(0, 0, 0, 0)
            self.layout.setSpacing(0)
            self.widget = QWidget()
            self.widget.setLayout(self.layout)
            self.splitter = QSplitter(Qt.Vertical)
            self.splitter1 = QSplitter(Qt.Vertical)
            self.splitter2 = QSplitter()
            self.__init_scintilla__()
            self.__init_output__()
            self.__init_debug__()

            self.splitter.addWidget(self.label)
            self.splitter.addWidget(self.scintilla)
            self.splitter.addWidget(self.output)
            self.splitter.setSizes((1,3,2))
            self.splitter1.addWidget(self.debug_label)
            self.splitter1.addWidget(self.debug)
            self.splitter1.setSizes((1,3))
            self.splitter2.addWidget(self.splitter)
            self.splitter2.addWidget(self.splitter1)
            self.splitter2.setSizes((1,1))
            self.splitter.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            self.setCentralWidget(self.splitter2)
            self.on_actionRestore_triggered()

        def __menubar__(self):
            self.menubar = QMenuBar(self)
            self.menubar.setGeometry(QRect(0, 0, 800, 34))
            self.menubar.setObjectName("menubar")
            self.menuFile = QMenu(self.menubar)
            self.menuFile.setObjectName("menuFile")
            self.menuEdit = QMenu(self.menubar)
            self.menuEdit.setObjectName("menuEdit")
            self.menuASM = QMenu(self.menubar)
            self.menuASM.setObjectName("menuASM")
            self.menuDisASM = QMenu(self.menubar)
            self.menuDisASM.setObjectName("menuDisASM")
            self.menuFont = QMenu(self.menubar)
            self.menuFont.setObjectName("menuFont")
            self.menuHelp = QMenu(self.menubar)
            self.menuHelp.setObjectName("menuHelp")
            self.setMenuBar(self.menubar)
            # self.statusbar = QStatusBar(self)
            # self.statusbar.setObjectName("statusbar")
            # self.setStatusBar(self.statusbar)
            # self.statusBar().setMaximumHeight(18)
            self.actionOpen = QAction(self)
            self.actionOpen.setObjectName("actionOpen")
            self.actionNew = QAction(self)
            self.actionNew.setObjectName("actionNew")
            self.actionSave = QAction(self)
            self.actionSave.setObjectName("actionSave")
            self.actionSave_As = QAction(self)
            self.actionSave_As.setObjectName("actionSave_As")
            self.actionPrint = QAction(self)
            self.actionPrint.setObjectName("actionPrint")
            self.actionExit = QAction(self)
            self.actionExit.setObjectName("actionExit")
            self.actionCut = QAction(self)
            self.actionCut.setObjectName("actionCut")
            self.actionCopy = QAction(self)
            self.actionCopy.setObjectName("actionCopy")
            self.actionPaste = QAction(self)
            self.actionPaste.setObjectName("actionPaste")
            self.actionDelete = QAction(self)
            self.actionDelete.setObjectName("actionDelete")
            self.actionFind = QAction(self)
            self.actionFind.setObjectName("actionFind")
            self.actionSelect_All = QAction(self)
            self.actionSelect_All.setObjectName("actionSelect_All")
            self.actionUndo = QAction(self)
            self.actionUndo.setObjectName("actionUndo")
            self.actionRedo = QAction(self)
            self.actionRedo.setObjectName("actionRedo")
            self.actionGenerate_bin = QAction(self)
            self.actionGenerate_bin.setObjectName("actionGenerate_bin")
            self.actionGenerate_coe = QAction(self)
            self.actionGenerate_coe.setObjectName("actionGenerate_coe")
            self.actionDebug_File = QAction(self)
            self.actionDebug_File.setObjectName("actionDebug_File")
            self.actionDebug_File_hex = QAction(self)
            self.actionDebug_File_hex.setObjectName("actionDebug_File_hex")
            self.actionLoad_bin = QAction(self)
            self.actionLoad_bin.setObjectName("actionLoad_bin")
            self.actionLoad_coe = QAction(self)
            self.actionLoad_coe.setObjectName("actionLoad_coe")
            self.actionAbout = QAction(self)
            self.actionAbout.setObjectName("actionAbout")
            self.actionColor = QAction(self)
            self.actionColor.setObjectName("actionColor")
            self.actionResize = QAction(self)
            self.actionResize.setObjectName("actionResize")
            self.actionFull = QAction(self)
            self.actionFull.setObjectName("actionFull")
            self.actionNormalWindow = QAction(self)
            self.actionNormalWindow.setObjectName("actionNormalWindow")
            self.actionMaximize = QAction(self)
            self.actionMaximize.setObjectName("actionMaximize")
            self.actionMinimize = QAction(self)
            self.actionMinimize.setObjectName("actionMinimize")
            self.actionRestore = QAction(self)
            self.actionRestore.setObjectName("actionRestore")
            self.menuFile.addAction(self.actionNew)
            self.menuFile.addAction(self.actionOpen)
            self.menuFile.addAction(self.actionSave)
            self.menuFile.addAction(self.actionSave_As)
            self.menuFile.addSeparator()
            self.menuFile.addAction(self.actionPrint)
            self.menuFile.addSeparator()
            self.menuFile.addAction(self.actionExit)
            self.menuEdit.addAction(self.actionUndo)
            self.menuEdit.addAction(self.actionRedo)
            self.menuEdit.addSeparator()
            self.menuEdit.addAction(self.actionCut)
            self.menuEdit.addAction(self.actionCopy)
            self.menuEdit.addAction(self.actionPaste)
            self.menuEdit.addAction(self.actionDelete)
            self.menuEdit.addAction(self.actionFind)
            self.menuEdit.addSeparator()
            self.menuEdit.addAction(self.actionSelect_All)
            self.menuASM.addAction(self.actionGenerate_bin)
            self.menuASM.addAction(self.actionGenerate_coe)
            self.menuASM.addAction(self.actionDebug_File)
            self.menuASM.addAction(self.actionDebug_File_hex)
            self.menuDisASM.addAction(self.actionLoad_bin)
            self.menuDisASM.addAction(self.actionLoad_coe)
            self.menuFont.addAction(self.actionColor)
            self.menuFont.addSeparator()
            self.menuFont.addAction(self.actionResize)
            self.menuFont.addSeparator()
            self.menuFont.addAction(self.actionFull)
            self.menuFont.addAction(self.actionNormalWindow)
            self.menuFont.addAction(self.actionMinimize)
            self.menuFont.addAction(self.actionMaximize)
            self.menuFont.addSeparator()
            self.menuFont.addAction(self.actionRestore)
            self.menuHelp.addAction(self.actionAbout)
            self.menubar.addAction(self.menuFile.menuAction())
            self.menubar.addAction(self.menuEdit.menuAction())
            self.menubar.addAction(self.menuASM.menuAction())
            self.menubar.addAction(self.menuDisASM.menuAction())
            self.menubar.addAction(self.menuFont.menuAction())
            self.menubar.addAction(self.menuHelp.menuAction())

            self.retranslateUi()
            QMetaObject.connectSlotsByName(self)

        def retranslateUi(self):
            _translate = QCoreApplication.translate
            self.menuFile.setTitle(_translate("self", "File"))
            self.menuEdit.setTitle(_translate("self", "Edit"))
            self.menuASM.setTitle(_translate("self", "ASM"))
            self.menuDisASM.setTitle(_translate("self", "DisASM"))
            self.menuFont.setTitle(_translate("self", "Font"))
            self.menuHelp.setTitle(_translate("self", "Help"))
            self.actionOpen.setText(_translate("self", "Open"))
            self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
            self.actionNew.setText(_translate("self", "New"))
            self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
            self.actionSave.setText(_translate("self", "Save"))
            self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
            self.actionSave_As.setText(_translate("self", "Save As.."))
            self.actionSave_As.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
            self.actionPrint.setText(_translate("self", "Print.."))
            self.actionPrint.setShortcut(_translate("MainWindow", "Ctrl+P"))
            self.actionExit.setText(_translate("self", "Exit.."))
            self.actionExit.setShortcut(_translate("MainWindow", "F4"))
            self.actionCut.setText(_translate("self", "Cut"))
            self.actionCut.setShortcut(_translate("MainWindow", "Ctrl+X"))
            self.actionCopy.setText(_translate("self", "Copy"))
            self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
            self.actionPaste.setText(_translate("self", "Paste"))
            self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))
            self.actionDelete.setText(_translate("self", "Delete"))
            self.actionFind.setText(_translate("self", "Find"))
            self.actionFind.setShortcut(_translate("MainWindow", "Ctrl+F"))
            self.actionSelect_All.setText(_translate("self", "Select All"))
            self.actionSelect_All.setShortcut(_translate("MainWindow", "Ctrl+A"))
            self.actionUndo.setText(_translate("self", "Undo"))
            self.actionUndo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
            self.actionRedo.setText(_translate("self", "Redo"))
            self.actionRedo.setShortcut(_translate("MainWindow", "Ctrl+Y"))
            self.actionGenerate_bin.setText(_translate("self", "Generate .bin"))
            self.actionGenerate_bin.setShortcut(_translate("MainWindow", "F6"))
            self.actionGenerate_coe.setText(_translate("self", "Generate .coe"))
            self.actionGenerate_coe.setShortcut(_translate("MainWindow", "F7"))
            self.actionDebug_File.setText(_translate("self", "Debug File(bin)"))
            self.actionDebug_File.setShortcut(_translate("MainWindow", "Ctrl+B"))
            self.actionDebug_File_hex.setText(_translate("self", "Debug File(hex)"))
            self.actionDebug_File_hex.setShortcut(_translate("MainWindow", "F8"))
            self.actionLoad_bin.setText(_translate("self", "Load .bin"))
            self.actionLoad_bin.setShortcut(_translate("MainWindow", "F9"))
            self.actionLoad_coe.setText(_translate("self", "Load .coe"))
            self.actionLoad_coe.setShortcut(_translate("MainWindow", "F10"))
            self.actionColor.setText(_translate("self", "Change Panel's Color"))
            self.actionResize.setText(_translate("self", "Resize"))
            self.actionResize.setShortcut(_translate("MainWindow", "F2"))
            self.actionFull.setText(_translate("self", "Full Screen"))
            self.actionFull.setShortcut(_translate("MainWindow", "F11"))
            self.actionMinimize.setText(_translate("self", "Minimize Window"))
            self.actionMinimize.setShortcut(_translate("MainWindow", "F2"))
            self.actionMaximize.setText(_translate("self", "Maximize Window"))
            self.actionMaximize.setShortcut(_translate("MainWindow", "F3"))
            self.actionNormalWindow.setText(_translate("self", "Normal Window"))
            self.actionNormalWindow.setShortcut(_translate("MainWindow", "F12"))
            self.actionRestore.setText(_translate("self", "Restore Default.."))
            self.actionAbout.setText(_translate("self", "About"))
            self.actionAbout.setShortcut(_translate("MainWindow", "F1"))

        def __init_output__(self):
            self.output = QsciScintilla()
            self.output.setUtf8(True)
            self.output.setFont(self.font)
            self.output.setMinimumSize(int(self.rect.width()/2.7),int(self.rect.height()/10))
            self.output.setMarginsFont(self.font)
            self.output.setMarginWidth(0, self.fontmetrics.width(str(self.scintilla.lines())) + 5)
            self.output.setMarginLineNumbers(0, True)
            self.output.setSelectionBackgroundColor(QColor("#606060"))
            self.output.setSelectionForegroundColor(QColor("#FFFFFF"))
            self.output.setMarginsBackgroundColor(QColor("#272727"))
            self.output.setMarginsForegroundColor(QColor("#CCCCCC"))
            self.output.setMarginWidth(1, 0)
            self.output.setMarginWidth(2, 0)
            self.output_lexer = output_Lexer(self.scintilla)
            self.output_lexer.setFont(self.font)
            self.output.setLexer(self.output_lexer)
            self.output.setText('Output : MIPS汇编器 @ 2018 浙江大学计算机系统小组 肖振新\n')

        def __init_debug__(self):
            self.debug = QsciScintilla()
            self.debug.setUtf8(True)
            self.debug.setFont(self.font)
            self.debug.setMinimumSize(int(self.rect.width()/6),int(self.rect.height()/3))
            self.debug.setMarginsFont(self.font)
            self.debug.setMarginWidth(0, self.fontmetrics.width(str(self.scintilla.lines())) + 5)
            self.debug.setMarginLineNumbers(0, True)
            self.debug.setSelectionBackgroundColor(QColor("#606060"))
            self.debug.setSelectionForegroundColor(QColor("#FFFFFF"))
            self.debug.setMarginsBackgroundColor(QColor("#272727"))
            self.debug.setMarginsForegroundColor(QColor("#CCCCCC"))
            self.debug.setMarginWidth(1, 0)
            self.debug.setMarginWidth(2, 0)
            self.debug_lexer = debug_Lexer(self.scintilla)
            self.debug_lexer.setFont(self.font)
            self.debug.setLexer(self.debug_lexer)
            self.debug.setText('Hint : you can hide Debug Console by\n'
                               ' dragging the boundary between them.')

        def __init_scintilla__(self):

            self.scintilla = QsciScintilla()
            self.scintilla.setUtf8(True)
            self.scintilla.setFont(self.font)
            self.scintilla.setMarginsFont(self.font)
            self.scintilla.setMinimumSize(int(self.rect.width()/2.7),int(self.rect.height()/3))
            #set line number width
            self.scintilla.setMarginWidth(0, self.fontmetrics.width(str(self.scintilla.lines())) + 5)
            self.scintilla.setMarginLineNumbers(0,True)
            #setEdge
            # self.scintilla.setEdgeMode(QsciScintilla.EdgeLine)
            # self.scintilla.setEdgeColumn(150)
            # self.scintilla.setEdgeColor(QColor("#BBB8B5"))

            #brace match
            self.scintilla.setBraceMatching(QsciScintilla.SloppyBraceMatch)

            #current line color
            self.scintilla.setCaretLineVisible(True)
            self.scintilla.setCaretLineBackgroundColor(QColor("#2D2D2D"))
            self.scintilla.setCaretForegroundColor(QColor("white"))

            #selection color
            self.scintilla.setSelectionBackgroundColor(QColor("#606060"))
            self.scintilla.setSelectionForegroundColor(QColor("#FFFFFF"))

            #table relative
            self.scintilla.setIndentationsUseTabs(True)
            self.scintilla.setIndentationWidth(int(self.font.pointSize()/3))
            self.scintilla.setTabIndents(True)
            self.scintilla.setAutoIndent(True)
            self.scintilla.setBackspaceUnindents(True)
            self.scintilla.setTabWidth(4)

            #indentation guides
            self.scintilla.setIndentationGuides(True)

            #line number margin color
            self.scintilla.setMarginsBackgroundColor(QColor("#272727"))
            self.scintilla.setMarginsForegroundColor(QColor("#CCCCCC"))

            #folding margin
            self.scintilla.setFolding(QsciScintilla.CircledTreeFoldStyle )
            self.scintilla.setMarginWidth(2,0)
            self.scintilla.resetFoldMarginColors()
            #self.scintilla.setFoldMarginColors(QColor("#555555"),QColor("#555555"))

            #marker
            self.scintilla.markerDefine(QsciScintilla.Minus,QsciScintilla.SC_MARKNUM_FOLDEROPEN)
            self.scintilla.markerDefine(QsciScintilla.Plus,QsciScintilla.SC_MARKNUM_FOLDER)
            self.scintilla.markerDefine(QsciScintilla.Minus,QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
            self.scintilla.markerDefine(QsciScintilla.Plus,QsciScintilla.SC_MARKNUM_FOLDEREND)

            #marker define color
            self.scintilla.setMarkerBackgroundColor(QColor("#FFFFFF"),QsciScintilla.SC_MARKNUM_FOLDEREND)
            self.scintilla.setMarkerForegroundColor(QColor("#272727"),QsciScintilla.SC_MARKNUM_FOLDEREND)
            self.scintilla.setMarkerBackgroundColor(QColor("#FFFFFF"),QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
            self.scintilla.setMarkerForegroundColor(QColor("#272727"),QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
            #self.scintilla.setMarkerBackgroundColor(QColor("#FFFFFF"),QsciScintilla.SC_MARKNUM_FOLDERMIDTAIL)
            #self.scintilla.setMarkerForegroundColor(QColor("#272727"),QsciScintilla.SC_MARKNUM_FOLDERMIDTAIL)
            #self.scintilla.setMarkerBackgroundColor(QColor("#FFFFFF"),QsciScintilla.SC_MARKNUM_FOLDERTAIL)
            #self.scintilla.setMarkerForegroundColor(QColor("#272727"),QsciScintilla.SC_MARKNUM_FOLDERTAIL)
            self.scintilla.setMarkerBackgroundColor(QColor("#FFFFFF"),QsciScintilla.SC_MARKNUM_FOLDERSUB)
            self.scintilla.setMarkerForegroundColor(QColor("#272727"),QsciScintilla.SC_MARKNUM_FOLDERSUB)
            self.scintilla.setMarkerBackgroundColor(QColor("#FFFFFF"),QsciScintilla.SC_MARKNUM_FOLDER)
            self.scintilla.setMarkerForegroundColor(QColor("#272727"),QsciScintilla.SC_MARKNUM_FOLDER)
            self.scintilla.setMarkerBackgroundColor(QColor("#FFFFFF"),QsciScintilla.SC_MARKNUM_FOLDEROPEN)
            self.scintilla.setMarkerForegroundColor(QColor("#272727"),QsciScintilla.SC_MARKNUM_FOLDEROPEN)
            self.scintilla.setFoldMarginColors(QColor("#272727"),QColor("#272727"))

            #whitespace
            self.scintilla.setWhitespaceVisibility(QsciScintilla.WsInvisible)
            self.scintilla.setWhitespaceSize(2)
            """
            the default margin is:

            0: line number,width is not zero
            1: width is zero
            2: folding, width is not zero

            """
            self.scintilla.setMarginWidth(1,0)
            #set lexer
            self.lexer = Lexer(self.scintilla)
            self.lexer.setFont(self.font)
            #self.lexer.setColor(QColor("#ffffff"))
            self.scintilla.setLexer(self.lexer)

            #self.lexer.setColor(QColor("#ffffff"))
            # self.lexer.setPaper(QColor("#333333"))
            # self.lexer.setColor(QColor("#5BA5F7"),QsciLexerPython.ClassName)

            self.scintilla.setMarginWidth(0, self.fontmetrics.width(str(self.scintilla.lines())) + 5)


def ReadStyleSheetFile( path ):
    ssf = QFile(path)
    ssf.open(QFile.ReadOnly)
    stream = QTextStream(ssf)
    return stream.readAll()

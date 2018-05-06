from gui.GUI import *
import sys
from gui.resource import *

if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = ScintillaEditor()

    icon = QIcon(':/resource/ASM/resource/icon.jpg')
    window.setWindowIcon(icon)
    scrollbar = ReadStyleSheetFile(":/resource/ASM/resource/stylesheet/scrollbar.css")
    scintilla = ReadStyleSheetFile(":/resource/ASM/resource/stylesheet/scintilla.css")
    common = ReadStyleSheetFile(":/resource/ASM/resource/stylesheet/common.css")
    stylesheet = scrollbar + scintilla + common
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    window.setStyleSheet(stylesheet)
    #window.scintilla.setText(open("/resource/test.s",encoding="UTF8").read())

    pixmap = QPixmap(":/resource/ASM/resource/open.jpg")
    pixmap = pixmap.scaled(int(pixmap.width() / 2), int(pixmap.height() / 2), Qt.IgnoreAspectRatio,
                         Qt.SmoothTransformation)
    screen = QSplashScreen(pixmap)
    screen.show()
    screen.showMessage("Loading necessary componets...", Qt.AlignBottom, Qt.black)
    timer = QElapsedTimer()
    timer.start()
    while (timer.elapsed() < int(0.7 * 1000)):pass
    screen.clearMessage()
    screen.showMessage("Initialing...", Qt.AlignBottom, Qt.black)
    while (timer.elapsed() < int(1.4 * 1000)):pass
    screen.clearMessage()
    screen.showMessage("Almost done...", Qt.AlignBottom, Qt.black)
    while (timer.elapsed() < int(2.1 * 1000)): pass
    screen.close()


    window.show()
    app.exec_()
    sys.exit()
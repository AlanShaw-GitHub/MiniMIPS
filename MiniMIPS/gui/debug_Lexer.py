from PyQt5.QtGui import *
from PyQt5.Qsci import *

class debug_Lexer(QsciLexerCustom):

    def __init__(self, parent):
        super(debug_Lexer, self).__init__(parent)

        self.setDefaultColor(QColor("#ff000000"))
        self.setDefaultPaper(QColor("#333333"))
        self.setColor(QColor("#00ff00"), 0)
        self.setPaper(QColor("#333333"), 0)  # Style 0: gray
        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), 0)  # Style 0: Consolas 14pt

    def language(self):
        return "SimpleLanguage"

    def description(self, style):
        if style == 0:
            return "myStyle_0"

    def styleText(self, start, end):
        self.startStyling(start)
        text = self.parent().text()[start:end]
        self.setStyling(len(text),0)

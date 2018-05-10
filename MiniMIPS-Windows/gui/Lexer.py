from PyQt5.QtGui import *
from PyQt5.Qsci import *
from utils.register import *
from assembler.functions import *
import re

class Lexer(QsciLexerCustom):

    def __init__(self, parent):
        super(Lexer, self).__init__(parent)

        # Default text settings
        # ----------------------
        self.setDefaultColor(QColor("#ff000000"))
        self.setDefaultPaper(QColor("#333333"))
        #self.setDefaultFont(QFont("Consolas", 14))

        # Initialize colors per style
        # ----------------------------
        self.setColor(QColor("#ffffff"), 0)
        self.setColor(QColor("#A462FF"), 1)
        self.setColor(QColor("#55C8A6"), 2)
        self.setColor(QColor("#808080"), 3)
        self.setColor(QColor("#DB5900"), 4)

        # Initialize paper colors per style
        # ----------------------------------
        self.setPaper(QColor("#333333"), 0)  # Style 0: gray
        self.setPaper(QColor("#333333"), 1)  # Style 1: gray
        self.setPaper(QColor("#333333"), 2)  # Style 2: gray
        self.setPaper(QColor("#333333"), 3)  # Style 3: gray
        self.setPaper(QColor("#333333"), 4)  # Style 3: gray

        # Initialize fonts per style
        # ---------------------------
        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), 0)  # Style 0: Consolas 14pt
        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), 1)  # Style 1: Consolas 14pt
        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), 2)  # Style 2: Consolas 14pt
        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), 3)  # Style 3: Consolas 14pt
        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), 4)  # Style 3: Consolas 14pt

    def language(self):
        return "SimpleLanguage"

    def description(self, style):
        if style == 0:
            return "myStyle_0"
        elif style == 1:
            return "myStyle_1"
        elif style == 2:
            return "myStyle_2"
        elif style == 3:
            return "myStyle_3"
        elif style == 4:
            return "myStyle_4"
        return ""

    def styleText(self, start, end):
        # 1. Initialize the styling procedure
        # ------------------------------------
        self.startStyling(start)

        # 2. Slice out a part from the text
        # ----------------------------------
        text = self.parent().text()[start:end]

        # 3. Tokenize the text
        # ---------------------
        #p = re.compile(r"0x[0-9]+|\$\w+|\n|[0-9]+|\.\w+|#")
        p = re.compile(r"\(|\)|\$\w+|\.\w+|\s+|\w+|\W")
        # 'token_list' is a list of tuples: (token_name, token_len)

        token_list = [(token, len(bytearray(token, "utf-8"))) for token in p.findall(text)]
        # 4. Style the text
        comm_flag = False

        # 4.2 Style the text in a loop
        for i, token in enumerate(token_list):
            if comm_flag:
                self.setStyling(token[1], 3)
                if re.match('\n',token[0]):
                    comm_flag = False
            else:
                if token[0] in register.keys():
                    self.setStyling(token[1], 1)
                elif token[0] in ['.data','.text','.byte','.word','.half','.ascii','.asciiz','.space']:
                    self.setStyling(token[1], 2)
                elif token[0] in functions.keys():
                    self.setStyling(token[1], 2)
                elif token[0] in ['(',')']:
                    self.setStyling(token[1], 2)
                elif re.match('0x',token[0]):
                    self.setStyling(token[1], 4)
                elif re.match('[0-9]+',token[0]):
                    self.setStyling(token[1], 4)
                elif re.match('"',token[0]):
                    self.setStyling(token[1], 4)
                elif token[0] == ':':
                    self.setStyling(token[1], 4)
                elif token[0] == "#":
                    comm_flag = True
                    self.setStyling(token[1], 3)
                else:
                    # Default style
                    self.setStyling(token[1], 0)

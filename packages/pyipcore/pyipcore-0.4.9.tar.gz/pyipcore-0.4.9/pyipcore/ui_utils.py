from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QGridLayout, QPushButton, QSpacerItem, QSizePolicy, QApplication
from PyQt5.Qsci import QsciScintilla, QsciLexerVerilog, QsciAPIs
from PyQt5.QtGui import QIcon, QPixmap, QDesktopServices, QFont, QColor
from pyipcore.ipc_utils import VERSION, GITEE_URL, APP_NAME
from rbpop import WinManager, RbpopInfo, RbpopWarn, RbpopError
from threading import Thread
import winsound
import time
import re


class QVerilogEdit(QsciScintilla):
    def __init__(self, parent=None, default_text=""):
        super().__init__(parent)

        # 创建 QScintilla 编辑器组件
        self.lexer = QsciLexerVerilog(parent)

        # 设置字体
        self.editor_font = QFont("Consolas", 14, QFont.Bold)
        self.editor_font.setFixedPitch(True)
        self.lexer.setFont(self.editor_font)
        self.setFont(self.editor_font)

        # 设置 lexer 为 Verilog
        self.setLexer(self.lexer)

        # 设置编辑器的大小和位置
        self.setGeometry(100, 100, 1400, 800)

        # 设置文本
        self.setText(default_text)

        # Set editor edit attributes
        self.set_editor_attributes()

        self._user_text_changed = None

    def set_editor_attributes(self):
        self.setUtf8(True)
        self.setMarginsFont(self.editor_font)
        self.setMarginWidth(0, len(str(len(self.text().split('\n')))) * 20)
        self.setMarginLineNumbers(0, True)

        self.setEdgeMode(QsciScintilla.EdgeLine)
        self.setEdgeColumn(100)
        self.setEdgeColor(QColor(0, 0, 0))

        self.setBraceMatching(QsciScintilla.StrictBraceMatch)

        self.setIndentationsUseTabs(True)
        self.setIndentationWidth(4)
        self.setTabIndents(True)
        self.setAutoIndent(True)
        self.setBackspaceUnindents(True)
        self.setTabWidth(4)

        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor('#FFFFCD'))

        self.setIndentationGuides(True)

        self.setFolding(QsciScintilla.PlainFoldStyle)
        self.setMarginWidth(2, 12)

        self.setMarkerForegroundColor(QColor("#272727"), QsciScintilla.SC_MARKNUM_FOLDEROPENMID)
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionCaseSensitivity(True)
        self.setAutoCompletionReplaceWord(False)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionUseSingle(QsciScintilla.AcusExplicit)

        self.__api = QsciAPIs(self.lexer)
        auto_completions = ['module', 'endmodule', 'input', 'output', 'inout', 'wire', 'reg', 'assign',
                           'always', 'posedge', 'negedge', 'if', 'else', 'begin', 'end',
                           'case', 'endcase', 'default', 'for', 'while', 'repeat', 'forever',
                           'initial', 'function', 'endfunction', 'task', 'endtask', 'logic', 'integer',
                           'parameter', 'localparam', 'generate', 'endgenerate']
        for word in auto_completions:
            self.__api.add(word)
        self.__api.prepare()
        self.autoCompleteFromAll()

        self.textChanged.connect(self.changed)

    def changed(self):
        self.setMarginWidth(0, len(str(len(self.text().split('\n')))) * 20)
        if self._user_text_changed:
            self._user_text_changed()

    def setUserTextChanged(self, func):
        self._user_text_changed = func



class BeepThread(Thread):
    def __init__(self):
        # 主程序退出后，子线程也退出
        super().__init__(daemon=True)
        self.tasks = []
        self.flag = True

    def Beep(self, freq, duration):
        self.tasks.append((freq, duration))

    def run(self):
        while self.flag:
            if not self.tasks:
                time.sleep(0.2)
                continue
            freq, duration = self.tasks.pop(0)
            winsound.Beep(freq, duration)

    def stop(self):
        self.flag = False


class BeepWinManager(WinManager):
    def __init__(self):
        super().__init__()
        self.beep = BeepThread()
        self.beep.start()

    def add(self, win, freq, duration):
        super().add(win)
        self.beep.Beep(freq, duration)


_GLOBAL_WM = [None]


def QPop(pop_win_inst, freq=400, duration=100):
    if _GLOBAL_WM[0] is None:
        _GLOBAL_WM[0] = BeepWinManager()

    _GLOBAL_WM[0].add(pop_win_inst, freq, duration)


def _pop_pre(title, msg):
    msg = re.sub(r'(.{30})', r'\1\n', ' ' + msg)
    _len = len(msg)
    ct = 4000 + _len * 50
    return title, msg, ct


def PopInfo(title, msg):
    title, msg, ct = _pop_pre(title, msg)
    QPop(RbpopInfo(msg, title, ct=ct, title_style='color:rgb(105,109,105);font-size:20px;', msg_style='color:rgb(65,98,65);font-size:20px;', close=True), 400, 300)


def PopWarn(title, msg):
    title, msg, ct = _pop_pre(title, msg)
    QPop(RbpopWarn(msg, title, ct=ct, title_style='color:rgb(105,125,85);font-size:20px;', msg_style='color:rgb(85,105,75);font-size:20px;', close=True), 600, 300)


def PopError(title, msg):
    title, msg, ct = _pop_pre(title, msg)
    QPop(RbpopError(msg, title, ct=ct, title_style='color:rgb(225,50,50);font-size:20px;', msg_style='color:rgb(185,50,50);font-size:20px;', close=True), 800, 300)


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.setWindowTitle(f"关于 {APP_NAME}")

        # 创建布局
        layout = QVBoxLayout()

        # 创建图标标签
        icon_label = QLabel(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icon/verilog.png"), QIcon.Normal, QIcon.Off)
        icon_label.setPixmap(icon.pixmap(128, 128))  # 设置图标大小

        # 创建文本标签
        self.text_label = QLabel(self)
        self.url_label = QLabel(self)
        self.set_text()  # 设置文本内容和链接
        self.text_label.setWordWrap(True)  # 开启文本换行
        self.url_label.setTextInteractionFlags(Qt.TextBrowserInteraction)  # 允许文本交互
        font = QApplication.font("SIMHEI")
        font.setPointSize(11)  # 例如，设置字号为12，您可以根据需要调整这个值
        self.text_label.setFont(font)
        self.url_label.setFont(font)

        # 创建按钮
        button = QPushButton("确定", self)
        button.setDefault(True)  # 设置为默认按钮

        # 创建网格布局并添加组件
        grid_layout = QGridLayout()
        grid_layout.addWidget(icon_label, 0, 0, 3, 1)  # 图标跨越3行
        grid_layout.addWidget(self.text_label, 0, 1, 1, 1)  # 文本标签在第一行，第二列
        grid_layout.addWidget(self.url_label, 1, 1, 1, 1)  # URL标签在第二行，第二列
        grid_layout.addWidget(button, 2, 1, 1, 1)  # 按钮在第三行，第二列

        # 添加水平间隔
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        grid_layout.addItem(spacer_item, 1, 0)

        # 将网格布局添加到垂直布局
        layout.addLayout(grid_layout)

        # 设置对话框的布局
        self.setLayout(layout)

        # 连接按钮的点击事件
        button.clicked.connect(self.close)

        # 连接文本标签的链接激活事件
        self.url_label.linkActivated.connect(self.open_url)

    def set_text(self):
        self.text_label.setText(f"Version: {VERSION}\n"
                                "Author: Eagle'sBaby，EAShine\n"
                                "Bilibili: 我阅读理解一直可以的\n"
                                "Bilibili UID: 129249826")
        # f"Gitee URL: <a href='{GITEE_URL}'>{GITEE_URL}</a>")
        self.url_label.setText(f"Gitee URL: <a href='{GITEE_URL}'>{GITEE_URL}</a>")
        self.url_label.setOpenExternalLinks(True)  # 允许打开外部链接

    def open_url(self, url):
        print(url)
        QDesktopServices.openUrl(QUrl(url))

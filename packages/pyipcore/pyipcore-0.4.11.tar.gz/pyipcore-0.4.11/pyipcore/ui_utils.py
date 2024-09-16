from PyQt5.QtCore import Qt, QUrl, QPoint, QRectF, QLineF, QPointF, QObject, QPropertyAnimation
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QGridLayout, QPushButton, QSpacerItem, QSizePolicy, QApplication
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsTextItem, QGraphicsPathItem, QGraphicsDropShadowEffect, QGraphicsPixmapItem
from PyQt5.Qsci import QsciScintilla, QsciLexerVerilog, QsciAPIs
from PyQt5.QtGui import QIcon, QPixmap, QDesktopServices, QFont, QColor, QPainter, QPen, QBrush, QPainterPath
from pyipcore.ipc_utils import VERSION, GITEE_URL, APP_NAME
from rbpop import WinManager, RbpopInfo, RbpopWarn, RbpopError
from threading import Thread
import winsound
import time
import math
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


class DraggableGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(DraggableGraphicsView, self).__init__(parent)
        self._raw_scene = QGraphicsScene()
        self.setScene(self._raw_scene)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.lastPos = QPoint()

    def wheelEvent(self, event):
        factor = 1.2
        if event.angleDelta().y() > 0:
            self.scale(factor, factor)
        else:
            self.scale(1 / factor, 1 / factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            delta = event.pos() - self.lastPos
            self.lastPos = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())

    def line(self, p0x, p0y, p1x, p1y, pcolor=Qt.black, width=1, *, dash=False):
        pen = QPen(QColor(pcolor), width)
        if dash:
            pen.setStyle(Qt.DashLine)
        line = QLineF(QPointF(p0x, p0y), QPointF(p1x, p1y))
        path = QPainterPath()
        path.moveTo(line.p1())
        path.lineTo(line.p2())
        item = QGraphicsPathItem(path)
        item.setPen(pen)
        self.scene().addItem(item)
        return item

    def rectangle(self, p0x, p0y, w, h, bcolor=Qt.black, width=1, fcolor=None, *, dash=False):
        pen = QPen(QColor(bcolor), width)
        if dash:
            pen.setStyle(Qt.DashLine)
        brush = QBrush(QColor(fcolor)) if fcolor else QBrush()
        rect = QRectF(p0x, p0y, w, h)
        # self.scene().addRect(rect, pen, brush)
        # return rect
        path = QPainterPath()
        path.addRect(rect)
        item = QGraphicsPathItem(path)
        item.setPen(pen)
        item.setBrush(brush)
        self.scene().addItem(item)
        return item

    def cycle(self, center_x, center_y, radius, pcolor=Qt.black, width=1, fcolor=None, *, dash=False):
        pen = QPen(QColor(pcolor), width)
        if dash:
            pen.setStyle(Qt.DashLine)
            pen.setDashPattern([5, 5])  # 设置虚线的样式，5个单位的线段后跟5个单位的空白
        brush = QBrush(QColor(fcolor)) if fcolor else QBrush()
        path = QPainterPath()
        path.addEllipse(center_x - radius, center_y - radius, 2 * radius, 2 * radius)
        item = QGraphicsPathItem(path)
        item.setPen(pen)
        item.setBrush(brush)
        self.scene().addItem(item)
        return item

    def text(self, text, x, y, font=None, font_color=Qt.black, *, dash=False, rotate=0, use_r=False, use_b=False):
        text_item = QGraphicsTextItem(text)
        if font:
            text_item.setFont(font)
        else:
            # 如果没有提供字体，可以设置默认字体属性
            default_font = QFont()
            default_font.setPointSize(12)  # 默认字体大小
            text_item.setFont(default_font)
        text_item.setDefaultTextColor(QColor(font_color))

        # 计算文本的宽度和高度
        text_width = text_item.boundingRect().width()
        text_height = text_item.boundingRect().height()

        # 计算旋转角度（弧度）
        rotate = rotate % 360
        theta = math.radians(rotate)

        if rotate == 0 or rotate == 180:
            new_width = text_width
            new_height = text_height
        elif rotate == 90 or rotate == 270:
            new_width = text_height
            new_height = text_width
        else:
            new_width = text_width * math.cos(theta) + text_height * math.sin(theta)
            new_height = text_width * math.sin(theta) + text_height * math.cos(theta)

        # 如果 use_rp 为 True，则将坐标调整为右上角
        if use_r:
            x -= new_width
        if use_b:
            y -= new_height

        text_item.setPos(x, y)
        text_item.setRotation(rotate)
        self.scene().addItem(text_item)
        return text_item

    def arrow(self, start_x, start_y, end_x, end_y, pen_color=Qt.black, pen_width=1, arrow_size=10, *, dash=False):
        pen = QPen(QColor(pen_color), pen_width)
        if dash:
            pen.setStyle(Qt.DashLine)
            pen.setDashPattern([5, 5])  # 设置虚线的样式，5个单位的线段后跟5个单位的空白
        else:
            pen.setStyle(Qt.SolidLine)

        # 创建箭头路径
        path = QPainterPath()
        dx, dy = end_x - start_x, end_y - start_y
        delta = math.sqrt(dx * dx + dy * dy)
        ratio = pen_width / delta
        path.moveTo(QPointF(start_x + dx * ratio * .25, start_y + dy * ratio * .25))
        path.lineTo(QPointF(end_x - dx * ratio, end_y - dy * ratio))

        # 计算箭头尖端的角度和位置
        angle = math.degrees(math.atan2(end_y - start_y, end_x - start_x))
        half_angle = (angle + 180 + 15) % 360  # 计算一个尖端的角度
        other_half_angle = (angle + 180 - 15) % 360  # 计算另一个尖端的角度

        # 箭头尖端的长度和宽度
        arrow_len = arrow_size
        arrow_width = pen_width * 2

        # 计算箭头尖端的两个点
        p1_x = end_x + arrow_len * math.cos(math.radians(half_angle))
        p1_y = end_y + arrow_len * math.sin(math.radians(half_angle))
        p2_x = end_x + arrow_len * math.cos(math.radians(other_half_angle))
        p2_y = end_y + arrow_len * math.sin(math.radians(other_half_angle))

        # 添加箭头尖端
        path.moveTo(QPointF(end_x, end_y))
        path.lineTo(QPointF(p1_x, p1_y))
        path.lineTo(QPointF(end_x, end_y))
        path.lineTo(QPointF(p2_x, p2_y))
        path.closeSubpath()

        arrow_item = QGraphicsPathItem(path)
        arrow_item.setPen(pen)
        self.scene().addItem(arrow_item)

        return arrow_item

    def clear(self):
        self.scene().clear()

    def remove(self, item):
        self.scene().removeItem(item)

    def effect_shallow(self, radius=15, offset_x=5, offset_y=5, color=Qt.darkGray):
        # 创建阴影效果对象
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(radius)  # 设置模糊半径
        shadow_effect.setOffset(offset_x, offset_y)
        shadow_effect.setColor(color)

        # 获取场景中的所有图形项
        items = self.scene().items()

        # 为每个图形项应用阴影效果
        for item in items:
            item.setGraphicsEffect(shadow_effect)

    def pixelize(self):
        """
        将图像像素化
        先render，清空场景，再添加像素化图像

        """
        # 渲染场景
        pixmap = QPixmap(self.scene().sceneRect().size().toSize())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        self.scene().render(painter)
        painter.end()

        # 清空场景
        self.scene().clear()

        # 添加像素化图像
        pixel_item = QGraphicsPixmapItem(pixmap)
        self.scene().addItem(pixel_item)

        return pixel_item

    def image(self, filename, x, y, width, height):
        pixmap = QPixmap(filename)
        pixmap = pixmap.scaled(width, height)
        item = QGraphicsPixmapItem(pixmap)
        item.setPos(x, y)
        self.scene().addItem(item)
        return item

    def save(self, filename):
        """
        保存场景为图片
        :param filename: 保存的文件名
        """
        pixmap = QPixmap(self.scene().sceneRect().size().toSize())
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        self.scene().render(painter)
        painter.end()
        pixmap.save(filename)


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

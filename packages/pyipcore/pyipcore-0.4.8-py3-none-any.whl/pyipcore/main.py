from pyipcore.ui_main import GUI_Main, QApplication, QMessageBox
import sys


def pyipc():
    """
    Run the GUI application.
    CMD主函数入口
    """
    app = QApplication(sys.argv)
    gui = GUI_Main()
    gui.show()
    try:
        sys.exit(app.exec_())
    except Exception as err:
        QMessageBox.warning(gui, "Error:", str(err))


if __name__ == '__main__':
    pyipc()

# _*_ coding:UTF-8 _*_
import win32con
import ctypes
import ctypes.wintypes
import threading
import pyautogui
from PyQt5 import QtCore, QtGui, QtWidgets
import inspect
import ctypes


# 窗口父类
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(420, 271)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setEnabled(False)
        self.textBrowser.setGeometry(QtCore.QRect(40, 20, 321, 31))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(70, 160, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(40, 70, 341, 19))
        self.checkBox.setObjectName("checkBox")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(230, 160, 93, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(200, 120, 72, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(120, 120, 41, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(80, 230, 41, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(140, 230, 231, 16))
        self.label_4.setText("暂无日志")
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.start)
        self.pushButton_2.clicked.connect(Form.stop)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "一键复制粘贴"))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">使用C键来代替Ctrl+C，使用V键来代替Ctrl+V</p></body></html>"))
        self.pushButton.setText(_translate("Form", "启用"))
        self.checkBox.setText(_translate("Form", "启用换行（粘贴之后自动按下Enter发送消息）"))
        self.pushButton_2.setText(_translate("Form", "停用"))
        self.label.setText(_translate("Form", "未启用"))
        self.label_2.setText(_translate("Form", "状态："))
        self.label_3.setText(_translate("Form", "Log:"))


# 窗口子类
class MyPyQT_Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(MyPyQT_Form, self).__init__()
        self.setupUi(self)
        self.hotkey = None

    # “启用”按钮绑定的函数
    def start(self):
        if self.label.text() != "已启用":
            self.hotkey = Hotkey()
            self.hotkey.start()
            self.label.setText("已启用")

    # “停用”按钮绑定的函数
    def stop(self):
        if self.hotkey:
            if self.hotkey.is_alive():
                stop_thread(self.hotkey)
                pyautogui.press('c')
                self.label.setText("未启用")

    # 窗口关闭事件
    def closeEvent(self, event):
        if self.hotkey:
            if self.hotkey.is_alive():
                stop_thread(self.hotkey)
                pyautogui.press('c')
        sys.exit(0)


# 创建一个Thread.threading扩展类,实例用来监听热键
class Hotkey(threading.Thread):
    def run(self):
        self.id1 = 105              # 注册热键的唯一id，用来区分热键
        self.id2 = 106
        self.user32 = ctypes.windll.user32                                # 加载user32.dll
        if not self.user32.RegisterHotKey(None, self.id1, 0, ord("C")):   # 注册快捷键C并判断是否成功
            my_pyqt_form.label_4.setText("无法注册热键C")                  # 在Label_4显示错误信息
        if not self.user32.RegisterHotKey(None, self.id2, 0, ord("V")):   # 注册快捷键V并判断是否成功
            my_pyqt_form.label_4.setText("无法注册热键V")
        # 检测热键是否被按下，并在出现异常时释放热键
        try:
            msg = ctypes.wintypes.MSG()
            # 循环读取消息
            while True:
                if self.user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                    if msg.message == win32con.WM_HOTKEY:
                        # 按下了热键C
                        if msg.wParam == self.id1:
                            # 调用copy()函数
                            self.copy()
                        # 按下了热键V
                        elif msg.wParam == self.id2:
                            # 调用paste()函数
                            self.paste()
                    self.user32.TranslateMessage(ctypes.byref(msg))
                    self.user32.DispatchMessageA(ctypes.byref(msg))
        # 释放热键，否则下次会注册失败
        finally:
            self.user32.UnregisterHotKey(None, self.id1)
            self.user32.UnregisterHotKey(None, self.id2)

    def copy(self):
        # 模拟按下Ctrl+C
        pyautogui.hotkey('ctrl', 'c')

    def paste(self):
        # 模拟按下Ctrl+V
        pyautogui.hotkey('ctrl', 'v')
        # 模拟按下Ctrl+V，如果启用了换行，则在模拟按下Enter
        if my_pyqt_form.checkBox.isChecked(): pyautogui.press('enter')


def _async_raise(tid, exctype):
    """Raises an exception in the threads with id tid"""
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    my_pyqt_form = MyPyQT_Form()
    my_pyqt_form.show()
    sys.exit(app.exec_())
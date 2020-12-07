import os

from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog
from PySide2.QtUiTools import QUiLoader
import sys
from PySide2.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PySide2.QtGui import QIcon
from PySide2.QtCore import QFile, Slot

import Test
import VoiceTransformToText
import Get_text_result
global path

class Stats:
    global path
    def __init__(self, parent=None):
        # 从文件中加载UI定义
        qfile_stats = QFile('315.ui')
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load(qfile_stats)
        self.ui.select_file.clicked.connect(self.openFileDialog)
        self.ui.start.clicked.connect(self.startVoiceTest)

    @Slot()
    def openFileDialog(self):
        # 生成文件对话框对象
        dialog = QFileDialog()
        # 设置文件过滤器，这里是任何文件，包括目录噢
        dialog.setFileMode(QFileDialog.AnyFile)
        # 设置显示文件的模式，这里是详细模式
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec_():
            fileNames = dialog.selectedFiles()
            self.ui.filepath.setText(fileNames[0])
            self.path = fileNames[0]

    @Slot()
    def startVoiceTest(self):
        a = self.path.split('/')
        filepath = ''
        for i in a:
            filepath = filepath + i + "\\" + '\\'
        filepath = filepath[:-2]
        print(filepath)
        s = Test.solve_start(filepath)
        QMessageBox.about(self.ui,
                          '语音质检结果',
                          f'''  此客服的态度为：{s}   '''
                          )


    def handleCalc(self):
        info = 1
        print(info)


app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()

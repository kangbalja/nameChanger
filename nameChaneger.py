# coding:utf-8

from PySide import QtCore, QtGui

import os
import sys

class NameChanger(QtGui.QWidget):
    
    def __init__(self):
        super(NameChanger, self).__init__()
        
        self.initUI()
        self.connectSignals()
    
    def initUI(self):
        
        mainLayout = QtGui.QVBoxLayout()
        
        self.dirButton = QtGui.QPushButton(u'폴더선택')
        
        # 경로
        formLayout = QtGui.QFormLayout()
        self.dirLabel = QtGui.QLabel(u'경로 :')
        self.dirLineEdit = QtGui.QLineEdit()
        self.dirLineEdit.setReadOnly(True)
        formLayout.addRow(self.tr("Path:"), self.dirLineEdit)
        
        self.namingCheckButton = QtGui.QPushButton(u'기존 네이밍 확인')
        self.namingList = QtGui.QTextEdit()
        self.namingList.setReadOnly(True)
        
        # 단어변경
        formLayout2 = QtGui.QFormLayout()
        self.oldWord = QtGui.QLineEdit()
        self.newWord = QtGui.QLineEdit()
        self.wordChangeButton = QtGui.QPushButton('Change')
        
        formLayout2.addRow(self.tr("Old  Word:"), self.oldWord)
        formLayout2.addRow(self.tr("New Word:"), self.newWord)
        formLayout2.addRow(self.wordChangeButton)
        
        self.namingList2 = QtGui.QTextEdit()
        self.namingList2.setReadOnly(True)
        
        # 메인 layout
        mainLayout.addWidget(self.dirButton)
        mainLayout.addLayout(formLayout)
        mainLayout.addWidget(self.namingCheckButton)
        mainLayout.addWidget(self.namingList)
        mainLayout.addLayout(formLayout2)
        mainLayout.addWidget(self.namingList2)
        
        # Widget 기본정보
        self.setLayout(mainLayout)
        self.setWindowTitle('NameChanger')
        self.setFixedWidth(600)
        self.show()
        
    def connectSignals(self):
        self.dirButton.clicked.connect(self.dirChoice)
        self.namingCheckButton.clicked.connect(self.namingCheck)
        self.wordChangeButton.clicked.connect(self.wordChange)
        
    def dirChoice(self):
        
        # 네이밍을 변환하고 싶은 디렉토리 선택
        self.selectedDir = QtGui.QFileDialog.getExistingDirectory()
        
        self.dirLineEdit.setText(self.selectedDir)
        
    def namingCheck(self):
        
        namingList = ''
        
        try:
            if self.selectedDir == '':
                QtGui.QMessageBox.critical (self, u'경고', u"폴더를 선택해주세요.", buttons=QtGui.QMessageBox.Ok, defaultButton=QtGui.QMessageBox.NoButton)
            else:
                for (path, dirs, files) in os.walk(self.selectedDir):
                    
                    dirs[:] = [dir for dir in dirs if dir != ".mayaSwatches"]
                    dirs[:] = [dir for dir in dirs if dir != "Keyboard"]
                    
                    for name in files:
                         namingList += os.path.join(path, name) + '\n'
                         
                self.namingList.setText(namingList)
                    
        except AttributeError:
            QtGui.QMessageBox.critical (self, u'경고', u"폴더를 선택해주세요.", buttons=QtGui.QMessageBox.Ok, defaultButton=QtGui.QMessageBox.NoButton)
            
            
    def wordChange(self):
        
        # 입력값 검사
        if self.oldWord.text() == '':
            QtGui.QMessageBox.critical (self, u'경고', u"old word를 입력해주세요.", buttons=QtGui.QMessageBox.Ok, defaultButton=QtGui.QMessageBox.NoButton)
            return
            
        if self.newWord.text() == '':
            QtGui.QMessageBox.critical (self, u'경고', u"new word를 입력해주세요.", buttons=QtGui.QMessageBox.Ok, defaultButton=QtGui.QMessageBox.NoButton)
            
        namingList = ''
        
        try:
            if self.selectedDir == '':
                QtGui.QMessageBox.critical (self, u'경고', u"폴더를 선택해주세요.", buttons=QtGui.QMessageBox.Ok, defaultButton=QtGui.QMessageBox.NoButton)
            else:
                for (path, dirs, files) in os.walk(self.selectedDir):
                    
                    dirs[:] = [dir for dir in dirs if dir != ".mayaSwatches"]
                    dirs[:] = [dir for dir in dirs if dir != "Keyboard"]
                    
                    for name in files:
                         
                        newFileName = name.replace(self.oldWord.text(), self.newWord.text())
                        
                        oldFullPath = os.path.join(path, name)
                        newFullPath = os.path.join(path, newFileName)
                        
                        if name != newFileName:
                            os.rename(oldFullPath, newFullPath)
                            namingList += "[SUCCESS] \n{0}".format(os.path.join(path, name)) + " \n> {0}".format(os.path.join(path, newFileName)) + '\n\n'
                        
                        
                        
                self.namingList2.setText(namingList)
                    
        except AttributeError:
            QtGui.QMessageBox.critical (self, u'경고', u"폴더를 선택해주세요.", buttons=QtGui.QMessageBox.Ok, defaultButton=QtGui.QMessageBox.NoButton)
         
    
def main():
    
    app = QtGui.QApplication(sys.argv)
    changer = NameChanger()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()


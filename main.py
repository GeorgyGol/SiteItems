#!/usr/bin/python3
# -*- coding: Cp1251 -*-

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMessageBox as msgbox, QFileDialog
import re

import sys
#import test_win
from db2pd import get_analitNotes, getNews, PandasModel, engine
from datetime import datetime

qtForm, qtBase=uic.loadUiType('test_win.ui')

class FirstWin(QtWidgets.QWidget, qtForm):
#class FirstWin(QMainWindow, qtForm):
    _isChange=False
    _currentIndex=None

    def readA(self):
        self.xTableW.setModel(PandasModel(get_analitNotes()))
        #self.xTableW.resizeColumnToContents(0)
        self.xTableW.resizeColumnsToContents()
        self.xTableW.resizeRowsToContents()
        self.xTableW.setColumnWidth(2, self.xTableW.columnWidth(2)/2)
        lst_cat=self.xTableW.model().dataframe()['A_Category'].unique().tolist().sort()
        self.cmdCategory.addItems(sorted(list(self.xTableW.model().dataframe()['A_Category'].unique())))
        self.flagChangeReset()
        self.xTableW.selectRow(0)
        self.clickedTA(self.xTableW.currentIndex())
        #self.xTableW.adjustSize()

    def MessageBox(self, icon=msgbox.Information, text='', infoText='', title='', detailText='',
                   buttons=(msgbox.Ok | msgbox.Cancel), bt_default=msgbox.Ok, bt_escape=msgbox.Cancel):
        msg=msgbox()
        msg.setIcon(icon)
        msg.setText(text)
        msg.setInformativeText(infoText)
        msg.setWindowTitle(title)
        msg.setDetailedText(detailText)
        msg.setStandardButtons(buttons)
        msg.setDefaultButton(bt_default)
        msg.setEscapeButton(bt_escape)
        return msg.exec_()

    def loadAnalit(self):
        pdfA = get_analitNotes().reset_index()
        pdfA.sort_values(by='A_Date', ascending=False, inplace=True, axis=0)

        self.xTableW.setColumnCount(len(pdfA.columns))
        for k, item in enumerate(pdfA.columns):
            self.xTableW.setHorizontalHeaderItem(k, QtWidgets.QTableWidgetItem(item))

        pdfA['A_Date'] = pdfA['A_Date'].dt.strftime('%d.%m.%Y')
        pdfA=pdfA.applymap(str)

        self.xTableW.setRowCount(pdfA.shape[0])
        for k, row in pdfA.iterrows():
            for n, item in enumerate(row):
                self.xTableW.setItem(k, n, QtWidgets.QTableWidgetItem(item))

    def clickedTA(self, index):
        if self._isChange:
            if self.saveRecord() == msgbox.Cancel:
                return

        self.xTableW.selectRow(index.row())
        #print(self.xTableW.selectedIndexes()[3].data())
        self._block_signals(flg=True)
        self.lblNum.setText(self.xTableW.selectedIndexes()[0].data())
        self.edtItem.setPlainText(self.xTableW.selectedIndexes()[2].data())
        self.dteItem.setDate(datetime.strptime (self.xTableW.selectedIndexes()[1].data(), '%d.%m.%Y'))
        self.edtURL.setText(self.xTableW.selectedIndexes()[4].data())
        self.spbPages.setValue(int(self.xTableW.selectedIndexes()[6].data()))
        self.chkVisible.setChecked(int(self.xTableW.selectedIndexes()[5].data()) !=0)
        self.cmdCategory.setCurrentText(self.xTableW.selectedIndexes()[3].data())
        self.lblStatus.setText('Current record: {}, records: {}'.format(self.xTableW.selectedIndexes()[0].data(),
                               self.xTableW.model().rowCount()))
        self._block_signals(flg=False)
        self._currentIndex=index



    def flagChangeReset(self):
        self._isChange = False
        self.btSave.setDisabled(True)
        self.btNew.setEnabled(True)

    def flagChange(self):
        self._isChange=True
        self.btSave.setEnabled(True)
        self.btNew.setDisabled(True)

    def saveRecord(self):
        def _askNotSave():
            if self._isChange:
                reply = msgbox.question(self, 'Имеются несохраненные записи', 'Сохранить изменения?',
                                        msgbox.Yes | msgbox.No | msgbox.Cancel, msgbox.Yes)
                return reply
            else:
                reply = msgbox.information(self, 'Just info', 'В Багдаде все спокойно',
                                           msgbox.Ok, msgbox.Ok)
                return reply

        def _makeQuery():
            strQ=''
            if self.lblNum.text() == 'NEW':
                strQ = '''INSERT INTO dbo.AnalitNotes
                (A_Date, A_Text, isVisible, A_Category, A_File, A_PageCount)
                VALUES ('{A_Date}', '{A_Text}', {isVisible}, '{A_Category}', '{A_File}', {A_PageCount}) 
                '''
            else:
                strQ = '''UPDATE dbo.AnalitNotes SET
                A_Date = '{A_Date}', 
                A_Text = '{A_Text}', 
                isVisible = {isVisible}, 
                A_Category = '{A_Category}', 
                A_File = '{A_File}', 
                A_PageCount = {A_PageCount}
                WHERE ID=''' + self.lblNum.text()

            return strQ.format(A_Date=self.dteItem.date().toPyDate(), A_Text=self.edtItem.toPlainText(),
                               A_File=self.edtURL.text(), A_Category=self.cmdCategory.currentText(),
                               isVisible=int(self.chkVisible.checkState()!=0), A_PageCount=self.spbPages.value())

        def _checkInput():
            ret_val= (not self.edtItem.toPlainText()) | (not self.edtURL.text())
            if ret_val:
                msgbox.warning(self, 'Error input ITEM parameters',
                           'Please check Item caption and Item URL - its must not be empty', msgbox.Ok)
                return False

            if self.spbPages.value()==0:
                r=msgbox.information(self, 'Error input ITEM parameters',
                                   'Please check Item page count = now it is 0', msgbox.Ok | msgbox.Cancel, msgbox.Cancel)
                if r==msgbox.Cancel:
                    return False

            if (self.cmdCategory.currentText() == 'NO') | (self.cmdCategory.currentText()==''):
                r = msgbox.information(self, 'Error input ITEM parameters',
                                       'Please check Item category param', msgbox.Ok | msgbox.Cancel,
                                       msgbox.Cancel)
                if r == msgbox.Cancel:
                    return False

            return True

        reply = _askNotSave()

        if reply == msgbox.No:
            msgbox.information(self, 'Just info', 'Will NOT save',
                       msgbox.Ok, msgbox.Ok)
            self.flagChangeReset()
        elif reply == msgbox.Yes:
            #msgbox.information(self, 'Just info', 'Will BE save',
            #           msgbox.Ok, msgbox.Ok)
            if not _checkInput():
                return msgbox.Cancel

            #print(self.edtURL.text().replace('\\', '/'))
            engine.execute(_makeQuery())


            self.flagChangeReset()
        else:
            self.xTableW.blockSignals(True)
            self.xTableW.selectRow(self._currentIndex.row())
            self.xTableW.blockSignals(False)

        return reply

    def _block_signals(self, flg=True):
        self.btnExit.blockSignals(flg)
        self.btSave.blockSignals(flg)
        self.dteItem.blockSignals(flg)
        self.cmdCategory.blockSignals(flg)
        self.edtItem.blockSignals(flg)
        self.edtURL.blockSignals(flg)
        self.spbPages.blockSignals(flg)
        self.chkVisible.blockSignals(flg)

    def _set_slots(self):
        self.dteItem.dateTimeChanged.connect(self.flagChange)
        self.cmdCategory.currentTextChanged.connect(self.flagChange)
        self.edtItem.textChanged.connect(self.flagChange)
        self.edtURL.textChanged.connect(self.flagChange)
        self.spbPages.editingFinished.connect((self.flagChange))
        self.chkVisible.stateChanged.connect((self.flagChange))

        # self.edtItem.activated.connect(self.flagChange)

    def getFileURL(self):
        #QFileDialog.getOpenFileUrl()
        options=QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        sStartDir=r'/run/user/1000/gvfs'
        fname=QFileDialog.getOpenFileName(self,
                                          'Select file', sStartDir,
                                          'Docs (*.pdf *.doc? *.xls?);;All files (*)', options=options)[0]
        if fname !='':
            self.edtURL.setText(re.sub(r'.+wwwroot', r'http://www.forecast.ru', fname.replace('\\', '/')))
            #print(re.sub(r'.+wwwroot', r'www.forecast.ru' ,fname ))



    def newRecord(self):
        self.lblNum.setText('NEW')
        self.edtItem.setPlainText('')
        self.dteItem.setDate(datetime.today())
        self.edtURL.setText('')
        self.spbPages.setValue(0)
        self.chkVisible.setChecked(True)
        self.cmdCategory.setCurrentText('NO')
        self.lblStatus.setText('Current record: {}, records: {}'.format('NEW',
                                                                self.xTableW.model().rowCount()))
        self.xTableW.clearSelection()

    def RefreshTable(self):
        self.xTableW.setModel(PandasModel(get_analitNotes()))
        self.flagChangeReset()
        self.xTableW.selectRow(self._currentIndex.row())
        self.clickedTA(self.xTableW.currentIndex())


    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.setupUi(self)

#        self.

        #self.mainLO.addStretch(1)
        #self.setLayout(self.mainLO)
        self.setWindowTitle('Сайт ЦМАКП: Аналитические записки')
        self.setLayout(self.backLO)
        self.btnExit.clicked.connect(QtWidgets.qApp.quit)
        self.xTableW.clicked.connect(self.clickedTA)
        self.btSave.clicked.connect(self.saveRecord)
        self.tlbURL.clicked.connect(self.getFileURL)
        self.btNew.clicked.connect(self.newRecord)
        self.btRefresh.clicked.connect(self.RefreshTable)
        self._set_slots()



app=QtWidgets.QApplication(sys.argv)
win=FirstWin()
#win.loadAnalit()
win.readA()
#win.setWindowOpacity(0.5)

win.show()
sys.exit(app.exec_())

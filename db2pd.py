#!/usr/bin/python3
# -*- coding: Cp1251 -*-

import sqlalchemy as sqal
import pandas as pd
from PyQt5 import QtCore

cstrConnectionString=r'mssql+pymssql://cmasf\web-db-writer:SorokTysjach0besian@L26-WWWSERVER/CMASF_WEB'

strTableAnalit='AnalitNotes'
strTableNews='News'

engine=sqal.create_engine(cstrConnectionString, connect_args={'charset':'cp1251'})

def get_analitNotes():
    lstrOrder=['ID', 'A_Date', 'A_Text', 'A_Category', 'A_File', 'isVisible', 'A_PageCount']
    return pd.read_sql_table(strTableAnalit, engine, parse_dates='A_Date')[lstrOrder].sort_values(by='A_Date', ascending=False)

def getNews():
    return pd.read_sql_table(strTableNews, engine, parse_dates=['NDate'], index_col='ID')

class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, df = pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        df['A_Date']=df['A_Date'].dt.strftime('%d.%m.%Y')
        self._df = df


    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        #print(self._df.columns.tolist()[section])
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return str(self._df.columns.tolist()[section])
            except (IndexError, ):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            return QtCore.QVariant()
            #try:
                # return self.df.index.tolist()
            #    return self._df.index.tolist()[section]
            #except (IndexError, ):
            #    return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):

        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        try:
            #print(self._df.index[index.row()])

            return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))
        except:
            return QtCore.QVariant()

    def setData(self, index, value, role):
        print('set data')
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype

            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return self._df.shape[0] #len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return self._df.shape[1] #len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

    def dataframe(self):
        return self._df


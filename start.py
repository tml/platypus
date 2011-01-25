""" A very rough sketch of where we need to go """
import wx

import wx.grid
import wx.stc as stc
import wx.lib.colourdb

import sqlite3 as sqlite
import simplejson as json

cursorDesc = {}
for i in enumerate(('name', 'type_code', 'display_size', 'internal_size', 'precision', 'scale', 'null_ok')):
    cursorDesc.update({i[1]:i[0]})
dbstr = """{"guru.db" : "%s"}""" % __PATH__
dbregistry = json.loads(dbstr)

class DBFrame(wx.Frame):
    def __init__(self, frameTitle="DB Demo", dataTable=None):
        self.frame = wx.Frame.__init__(self, None, -1, frameTitle, size=(400, 300))
        grid = wx.grid.Grid(self)
        grid.SetDefaultCellOverflow(False)
        if dataTable is None:
            dataTable = TestTable(cols)
        grid.SetTable(dataTable, True)
        for idx in range(grid.GetNumberCols()):
            grid.AutoSizeColLabelSize(idx)
        grid.AutoSizeColumns(setAsMin=False)
        grid.AutoSizeRows(setAsMin=False)

class MyEditor(stc.StyledTextCtrl):
    fold_symbols = 2

class TestTable(wx.grid.PyGridTableBase):
    data = {}
    def __init__(self, cols=None, rows=None):
        self.cols = cols
        currentRow = 0
        for (rowIdx, row) in enumerate(rows):
            for colIdx in range(len(self.cols)):
                self.data.update({(rowIdx, colIdx): row[colIdx]})
        (self.rowCount, self.colCount) = (rowIdx+1, colIdx+1)
        wx.grid.PyGridTableBase.__init__(self)
        self.odd=wx.grid.GridCellAttr()
        self.odd.SetBackgroundColour("sea green")
        self.odd.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.odd.SetOverflow(False)
        self.even=wx.grid.GridCellAttr()
        self.even.SetBackgroundColour(wx.Colour(240, 255, 170, 250))
        self.even.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.even.SetOverflow(False)

    def GetNumberRows(self):
        return self.rowCount

    def GetNumberCols(self):
        return self.colCount

    def IsEmptyCell(self, row, col):
        return self.data.get((row, col)) is not None

    def GetValue(self, row, col):
        value = self.data.get((row, col))
        if value is not None:
            return value
        else:
            return '(null)'

    def SetValue(self, row, col, value):
        self.data[(row,col)] = value

    def GetColLabelValue(self, idx):
        if self.cols is not None:
            label = self.cols[idx]
            return label

    def GetAttr(self, row, col, kind):
        attr = [self.even, self.odd][row % 2]
        attr.IncRef()
        return attr

    

if __name__ == '__main__':
    db = sqlite.connect(dbregistry['guru.db'])
    cursor = db.cursor()
    cursor.execute(__QUERY__)
    app = wx.PySimpleApp()
    display = []
    for seq in cursor.description:
        display.append(seq[cursorDesc['name']])
    table = TestTable(cols=display, rows=cursor)
    frame = DBFrame(dataTable=table)
    frame.Show()
    app.MainLoop()

import openpyxl

class IterData():
 def __init__(self, raw):
  self._raw = raw
  self._dataSet1 = None
  self._dataSet2 = None
  self._dataSet3 = None
 
 def iterRead(self):
  wb = openpyxl.load_workbook(filename=self._raw, read_only=True)
  self._dataSet1 = wb['Set1'] 
  self._dataSet2 = wb['Set2']
  self._dataSet3 = wb['Set3']

 
  






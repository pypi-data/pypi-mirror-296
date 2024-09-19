import jpype 
from asposepdf import Assist 


class PdfASymbolicFontEncodingStrategy_QueueItem_CMapEncodingTableType(Assist.BaseJavaClass):
    """!Declares set of some known encoding subtables"""

    java_class_name = "com.aspose.python.pdf.PdfASymbolicFontEncodingStrategy.QueueItem.CMapEncodingTableType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _WindowsUnicodeTable = 0
    _WindowsSymbolicTable = 1
    _MacTable = 2
    _UnicodeTable = 3

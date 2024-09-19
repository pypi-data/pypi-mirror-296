import jpype 
from asposepdf import Assist 


class PdfASymbolicFontEncodingStrategy_QueueItem(Assist.BaseJavaClass):
    """!Specifies encoding subtable. Each encoding subtable has unique combination of parameters
     (PlatformID, PlatformSpecificID). Enumeration {@code CMapEncodingTableType} and property
     {@code CMapEncodingTable} were implemented to make easier set of encoding subtable needed."""

    java_class_name = "com.aspose.python.pdf.PdfASymbolicFontEncodingStrategy.QueueItem"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

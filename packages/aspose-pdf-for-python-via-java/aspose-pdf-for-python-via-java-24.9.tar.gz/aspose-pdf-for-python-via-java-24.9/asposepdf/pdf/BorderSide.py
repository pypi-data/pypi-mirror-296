import jpype 
from asposepdf import Assist 


class BorderSide(Assist.BaseJavaClass):
    """!Flags
     Enumerates binary the border sides."""

    java_class_name = "com.aspose.python.pdf.BorderSide"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _All = 15
    _Left = 1
    _Top = 2
    _Right = 4
    _Bottom = 8
    _Box = 15
    _None = 0

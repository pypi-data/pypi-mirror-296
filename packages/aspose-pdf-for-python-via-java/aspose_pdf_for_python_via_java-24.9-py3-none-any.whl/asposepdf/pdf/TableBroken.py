import jpype 
from asposepdf import Assist 


class TableBroken(Assist.BaseJavaClass):
    """!Enumerates the table broken."""

    java_class_name = "com.aspose.python.pdf.TableBroken"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Vertical = 1
    _VerticalInSamePage = 2
    _None = 0
    _IsInNextPage = 3

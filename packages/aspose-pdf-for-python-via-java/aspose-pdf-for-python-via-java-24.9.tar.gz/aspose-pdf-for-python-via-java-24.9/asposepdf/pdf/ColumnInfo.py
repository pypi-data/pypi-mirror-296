import jpype 
from asposepdf import Assist 


class ColumnInfo(Assist.BaseJavaClass):
    """!This class represents a columns info."""

    java_class_name = "com.aspose.python.pdf.ColumnInfo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

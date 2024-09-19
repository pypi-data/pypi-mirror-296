import jpype 
from asposepdf import Assist 


class Cells(Assist.BaseJavaClass):
    """!Represents a cells collection of row."""

    java_class_name = "com.aspose.python.pdf.Cells"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

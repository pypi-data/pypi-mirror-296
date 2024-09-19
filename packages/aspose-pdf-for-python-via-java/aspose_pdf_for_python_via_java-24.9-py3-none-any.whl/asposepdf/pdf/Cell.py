import jpype 
from asposepdf import Assist 


class Cell(Assist.BaseJavaClass):
    """!Represents a cell of the table's row."""

    java_class_name = "com.aspose.python.pdf.Cell"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

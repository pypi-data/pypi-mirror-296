import jpype 
from asposepdf import Assist 


class Row(Assist.BaseJavaClass):
    """!Represents a row of the table."""

    java_class_name = "com.aspose.python.pdf.Row"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

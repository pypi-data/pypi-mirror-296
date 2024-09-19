import jpype 
from asposepdf import Assist 


class Table(Assist.BaseJavaClass):
    """!Represents a table that can be added to the page."""

    java_class_name = "com.aspose.python.pdf.Table"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

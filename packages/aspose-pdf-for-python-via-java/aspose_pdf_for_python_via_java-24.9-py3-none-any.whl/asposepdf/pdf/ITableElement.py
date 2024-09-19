import jpype 
from asposepdf import Assist 


class ITableElement(Assist.BaseJavaClass):
    """!This interface represents an element of existing table extracted by TableAbsorber."""

    java_class_name = "com.aspose.python.pdf.ITableElement"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

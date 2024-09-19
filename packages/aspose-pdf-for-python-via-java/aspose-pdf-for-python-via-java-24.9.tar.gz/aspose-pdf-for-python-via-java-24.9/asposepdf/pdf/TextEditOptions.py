import jpype 
from asposepdf import Assist 


class TextEditOptions(Assist.BaseJavaClass):
    """!Descubes options of text edit operations."""

    java_class_name = "com.aspose.python.pdf.TextEditOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

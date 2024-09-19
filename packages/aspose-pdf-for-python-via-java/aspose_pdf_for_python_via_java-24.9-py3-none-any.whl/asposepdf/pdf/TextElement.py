import jpype 
from asposepdf import Assist 


class TextElement(Assist.BaseJavaClass):
    """!General text element of document logical structure."""

    java_class_name = "com.aspose.python.pdf.TextElement"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

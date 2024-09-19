import jpype 
from asposepdf import Assist 


class SelectorRendition(Assist.BaseJavaClass):
    """!Class describes selector rendition."""

    java_class_name = "com.aspose.python.pdf.SelectorRendition"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

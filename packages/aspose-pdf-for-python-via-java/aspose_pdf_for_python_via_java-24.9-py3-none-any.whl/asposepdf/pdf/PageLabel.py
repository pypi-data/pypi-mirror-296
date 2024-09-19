import jpype 
from asposepdf import Assist 


class PageLabel(Assist.BaseJavaClass):
    """!Class representing Page Label range."""

    java_class_name = "com.aspose.python.pdf.PageLabel"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

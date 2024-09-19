import jpype 
from asposepdf import Assist 


class FontSource(Assist.BaseJavaClass):
    """!Represents a base class fot font source."""

    java_class_name = "com.aspose.python.pdf.FontSource"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

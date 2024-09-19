import jpype 
from asposepdf import Assist 


class Watermark(Assist.BaseJavaClass):
    """!Represents a watermark of the page."""

    java_class_name = "com.aspose.python.pdf.Watermark"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

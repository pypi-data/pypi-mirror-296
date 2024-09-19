import jpype 
from asposepdf import Assist 


class RichMediaAnnotation_ContentType(Assist.BaseJavaClass):
    """!Type of the multimedia."""

    java_class_name = "com.aspose.python.pdf.RichMediaAnnotation.ContentType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Unknown = 2
    _Video = 1
    _Audio = 0

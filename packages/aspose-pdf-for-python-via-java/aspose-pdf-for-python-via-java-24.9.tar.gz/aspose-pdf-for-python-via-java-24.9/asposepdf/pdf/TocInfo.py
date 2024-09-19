import jpype 
from asposepdf import Assist 


class TocInfo(Assist.BaseJavaClass):
    """!Represents table of contents info."""

    java_class_name = "com.aspose.python.pdf.TocInfo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

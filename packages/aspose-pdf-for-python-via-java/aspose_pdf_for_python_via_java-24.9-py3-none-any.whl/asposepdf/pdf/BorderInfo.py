import jpype 
from asposepdf import Assist 


class BorderInfo(Assist.BaseJavaClass):
    """!This class represents border for graphics elements."""

    java_class_name = "com.aspose.python.pdf.BorderInfo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

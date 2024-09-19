import jpype 
from asposepdf import Assist 


class Border(Assist.BaseJavaClass):
    """!Class representing characteristics of annotation border."""

    java_class_name = "com.aspose.python.pdf.Border"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

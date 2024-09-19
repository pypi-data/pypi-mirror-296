import jpype 
from asposepdf import Assist 


class Image(Assist.BaseJavaClass):
    """!Represents image."""

    java_class_name = "com.aspose.python.pdf.Image"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

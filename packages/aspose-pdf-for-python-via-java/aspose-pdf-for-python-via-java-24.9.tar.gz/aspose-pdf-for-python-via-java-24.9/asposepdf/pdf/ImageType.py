import jpype 
from asposepdf import Assist 


class ImageType(Assist.BaseJavaClass):
    """!Represents image format types."""

    java_class_name = "com.aspose.python.pdf.ImageType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

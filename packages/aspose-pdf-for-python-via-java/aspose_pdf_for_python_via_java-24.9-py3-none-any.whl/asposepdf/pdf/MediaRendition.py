import jpype 
from asposepdf import Assist 


class MediaRendition(Assist.BaseJavaClass):
    """!Class describes media rendition."""

    java_class_name = "com.aspose.python.pdf.MediaRendition"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class MediaClip(Assist.BaseJavaClass):
    """!Class describes media clip object of rendition."""

    java_class_name = "com.aspose.python.pdf.MediaClip"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

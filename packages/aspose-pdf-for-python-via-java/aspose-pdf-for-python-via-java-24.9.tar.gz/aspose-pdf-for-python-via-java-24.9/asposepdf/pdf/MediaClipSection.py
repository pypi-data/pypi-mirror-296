import jpype 
from asposepdf import Assist 


class MediaClipSection(Assist.BaseJavaClass):
    """!This class descibes Media clip section."""

    java_class_name = "com.aspose.python.pdf.MediaClipSection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

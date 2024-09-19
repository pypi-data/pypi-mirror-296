import jpype 
from asposepdf import Assist 


class BackgroundArtifact(Assist.BaseJavaClass):
    """!Class descibes background artifact. This artifact allows to set background of the page."""

    java_class_name = "com.aspose.python.pdf.BackgroundArtifact"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class HeaderArtifact(Assist.BaseJavaClass):
    """!Class describes Heaader artifact. This artifacgt may be used to set heading of the page."""

    java_class_name = "com.aspose.python.pdf.HeaderArtifact"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

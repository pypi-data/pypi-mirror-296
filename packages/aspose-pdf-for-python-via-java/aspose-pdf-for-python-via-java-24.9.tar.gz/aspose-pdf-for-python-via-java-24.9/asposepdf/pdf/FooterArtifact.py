import jpype 
from asposepdf import Assist 


class FooterArtifact(Assist.BaseJavaClass):
    """!Describes footer artifact. This may be used to set footer of the page."""

    java_class_name = "com.aspose.python.pdf.FooterArtifact"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

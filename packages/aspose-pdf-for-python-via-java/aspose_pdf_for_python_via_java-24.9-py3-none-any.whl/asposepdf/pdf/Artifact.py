import jpype 
from asposepdf import Assist 


class Artifact(Assist.BaseJavaClass):
    """!Class represents PDF Artifact object."""

    java_class_name = "com.aspose.python.pdf.Artifact"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class ArtifactCollection(Assist.BaseJavaClass):
    """!Class represents artifact collection."""

    java_class_name = "com.aspose.python.pdf.ArtifactCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

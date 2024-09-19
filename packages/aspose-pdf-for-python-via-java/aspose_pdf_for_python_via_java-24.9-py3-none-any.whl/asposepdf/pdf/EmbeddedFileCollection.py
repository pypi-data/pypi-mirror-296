import jpype 
from asposepdf import Assist 


class EmbeddedFileCollection(Assist.BaseJavaClass):
    """!Class representing embedded files collection."""

    java_class_name = "com.aspose.python.pdf.EmbeddedFileCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class FileSpecification(Assist.BaseJavaClass):
    """!Class representing embedded file."""

    java_class_name = "com.aspose.python.pdf.FileSpecification"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

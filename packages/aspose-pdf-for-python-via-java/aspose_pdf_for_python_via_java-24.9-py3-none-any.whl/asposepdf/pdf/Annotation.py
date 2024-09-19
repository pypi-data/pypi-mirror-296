import jpype 
from asposepdf import Assist 


class Annotation(Assist.BaseJavaClass):
    """!Class representing annotation object."""

    java_class_name = "com.aspose.python.pdf.Annotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

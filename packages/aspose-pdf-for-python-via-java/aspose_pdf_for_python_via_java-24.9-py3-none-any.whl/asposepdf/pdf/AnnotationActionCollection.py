import jpype 
from asposepdf import Assist 


class AnnotationActionCollection(Assist.BaseJavaClass):
    """!Represents the collection of annotation actions."""

    java_class_name = "com.aspose.python.pdf.AnnotationActionCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

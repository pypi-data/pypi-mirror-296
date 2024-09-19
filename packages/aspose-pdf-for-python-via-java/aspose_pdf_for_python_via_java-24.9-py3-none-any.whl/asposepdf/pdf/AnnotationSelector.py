import jpype 
from asposepdf import Assist 


class AnnotationSelector(Assist.BaseJavaClass):
    """!This class is used for selecting annotations using Visitor template idea."""

    java_class_name = "com.aspose.python.pdf.AnnotationSelector"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

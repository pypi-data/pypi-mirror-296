import jpype 
from asposepdf import Assist 


class Paragraphs(Assist.BaseJavaClass):
    """!This class represents paragraph collection."""

    java_class_name = "com.aspose.python.pdf.Paragraphs"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

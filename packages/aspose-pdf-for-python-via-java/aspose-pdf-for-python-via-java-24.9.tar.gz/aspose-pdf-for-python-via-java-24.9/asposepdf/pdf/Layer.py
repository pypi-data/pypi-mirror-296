import jpype 
from asposepdf import Assist 


class Layer(Assist.BaseJavaClass):
    """!Represents a layer within a PDF page."""

    java_class_name = "com.aspose.python.pdf.Layer"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

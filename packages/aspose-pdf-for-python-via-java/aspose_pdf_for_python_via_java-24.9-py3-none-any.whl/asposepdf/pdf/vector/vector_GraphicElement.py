import jpype 
from asposepdf import Assist 


class vector_GraphicElement(Assist.BaseJavaClass):
    """!Represents base class for graphics object on the page."""

    java_class_name = "com.aspose.python.pdf.vector.GraphicElement"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

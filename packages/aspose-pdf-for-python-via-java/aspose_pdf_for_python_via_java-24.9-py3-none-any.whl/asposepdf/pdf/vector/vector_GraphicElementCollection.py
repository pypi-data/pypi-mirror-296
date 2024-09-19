import jpype 
from asposepdf import Assist 


class vector_GraphicElementCollection(Assist.BaseJavaClass):
    """!Represents {@link GraphicElement} collection."""

    java_class_name = "com.aspose.python.pdf.vector.GraphicElementCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

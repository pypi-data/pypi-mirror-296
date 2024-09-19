import jpype 
from asposepdf import Assist 


class vector_GraphicState(Assist.BaseJavaClass):
    """!Represents graphic state of the current {@link GraphicElement}."""

    java_class_name = "com.aspose.python.pdf.vector.GraphicState"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

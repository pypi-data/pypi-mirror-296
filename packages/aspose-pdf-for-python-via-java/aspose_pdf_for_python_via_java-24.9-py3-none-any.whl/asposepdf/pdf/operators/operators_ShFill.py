import jpype 
from asposepdf import Assist 


class operators_ShFill(Assist.BaseJavaClass):
    """!Class representing sh operator (paint area with shading pattern)."""

    java_class_name = "com.aspose.python.pdf.operators.ShFill"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

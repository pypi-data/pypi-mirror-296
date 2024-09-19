import jpype 
from asposepdf import Assist 


class operators_ObsoleteFill(Assist.BaseJavaClass):
    """!Class representing F operator (fill path using nonzero winding rule)."""

    java_class_name = "com.aspose.python.pdf.operators.ObsoleteFill"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

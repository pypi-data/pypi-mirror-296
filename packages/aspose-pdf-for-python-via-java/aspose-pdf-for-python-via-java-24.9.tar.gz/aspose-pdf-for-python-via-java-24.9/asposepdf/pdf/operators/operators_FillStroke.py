import jpype 
from asposepdf import Assist 


class operators_FillStroke(Assist.BaseJavaClass):
    """!Class representing B operator (fill and stroke path using nonzero winding rule)"""

    java_class_name = "com.aspose.python.pdf.operators.FillStroke"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class operators_BT(Assist.BaseJavaClass):
    """!Class representing BT operator (Begin of text block)."""

    java_class_name = "com.aspose.python.pdf.operators.BT"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class operators_ConcatenateMatrix(Assist.BaseJavaClass):
    """!Class representing cm operator (concatenate matrix to current transformation matrix)."""

    java_class_name = "com.aspose.python.pdf.operators.ConcatenateMatrix"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

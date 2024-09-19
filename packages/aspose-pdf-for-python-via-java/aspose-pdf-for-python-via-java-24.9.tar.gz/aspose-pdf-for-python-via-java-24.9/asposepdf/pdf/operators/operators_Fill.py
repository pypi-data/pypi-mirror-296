import jpype 
from asposepdf import Assist 


class operators_Fill(Assist.BaseJavaClass):
    """!Class representing f operator (fill path with nonzero winding number rule)."""

    java_class_name = "com.aspose.python.pdf.operators.Fill"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class operators_EOFill(Assist.BaseJavaClass):
    """!Class representing f* operator (fill path using even-odd rule)."""

    java_class_name = "com.aspose.python.pdf.operators.EOFill"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class operators_SelectFont(Assist.BaseJavaClass):
    """!Class representing Tf operator (set text font and size)."""

    java_class_name = "com.aspose.python.pdf.operators.SelectFont"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

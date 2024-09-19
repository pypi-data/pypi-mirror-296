import jpype 
from asposepdf import Assist 


class operators_LineTo(Assist.BaseJavaClass):
    """!Class representing l operator (add line to the path)."""

    java_class_name = "com.aspose.python.pdf.operators.LineTo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

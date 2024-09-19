import jpype 
from asposepdf import Assist 


class operators_Re(Assist.BaseJavaClass):
    """!Class representing re operator (add rectangle to the path)."""

    java_class_name = "com.aspose.python.pdf.operators.Re"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

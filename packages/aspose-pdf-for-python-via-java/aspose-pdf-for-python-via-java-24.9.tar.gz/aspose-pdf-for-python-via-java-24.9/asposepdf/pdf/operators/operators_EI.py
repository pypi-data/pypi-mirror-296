import jpype 
from asposepdf import Assist 


class operators_EI(Assist.BaseJavaClass):
    """!Class representing EI operator (End inline image object)."""

    java_class_name = "com.aspose.python.pdf.operators.EI"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

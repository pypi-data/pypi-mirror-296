import jpype 
from asposepdf import Assist 


class operators_EX(Assist.BaseJavaClass):
    """!Class representing EX operator (End of compatibility section)."""

    java_class_name = "com.aspose.python.pdf.operators.EX"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

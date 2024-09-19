import jpype 
from asposepdf import Assist 


class operators_GRestore(Assist.BaseJavaClass):
    """!Class representing Q operator (restore graphics state)."""

    java_class_name = "com.aspose.python.pdf.operators.GRestore"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

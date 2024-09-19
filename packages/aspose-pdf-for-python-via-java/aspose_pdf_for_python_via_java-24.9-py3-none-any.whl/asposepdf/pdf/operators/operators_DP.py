import jpype 
from asposepdf import Assist 


class operators_DP(Assist.BaseJavaClass):
    """!Class represeting DP operator (designamte marked content point)."""

    java_class_name = "com.aspose.python.pdf.operators.DP"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

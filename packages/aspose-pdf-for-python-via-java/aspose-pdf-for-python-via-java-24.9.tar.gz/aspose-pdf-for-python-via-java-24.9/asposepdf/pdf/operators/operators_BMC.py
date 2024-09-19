import jpype 
from asposepdf import Assist 


class operators_BMC(Assist.BaseJavaClass):
    """!Class representing BMC operator (Begin marked-content sequence)."""

    java_class_name = "com.aspose.python.pdf.operators.BMC"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

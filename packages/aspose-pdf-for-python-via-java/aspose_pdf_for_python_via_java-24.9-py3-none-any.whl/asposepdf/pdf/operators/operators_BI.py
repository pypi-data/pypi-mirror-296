import jpype 
from asposepdf import Assist 


class operators_BI(Assist.BaseJavaClass):
    """!Class representing BI operator (Begin inline image obect)."""

    java_class_name = "com.aspose.python.pdf.operators.BI"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

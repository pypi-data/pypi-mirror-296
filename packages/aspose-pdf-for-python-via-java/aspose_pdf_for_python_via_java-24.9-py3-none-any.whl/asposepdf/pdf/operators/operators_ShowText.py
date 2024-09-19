import jpype 
from asposepdf import Assist 


class operators_ShowText(Assist.BaseJavaClass):
    """!Class representing Tj operator (show text)."""

    java_class_name = "com.aspose.python.pdf.operators.ShowText"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

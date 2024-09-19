import jpype 
from asposepdf import Assist 


class operators_ET(Assist.BaseJavaClass):
    """!Class representing operator ET (End of text block)."""

    java_class_name = "com.aspose.python.pdf.operators.ET"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

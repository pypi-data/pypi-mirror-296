import jpype 
from asposepdf import Assist 


class operators_EndPath(Assist.BaseJavaClass):
    """!Class representing n operator (end path without filling or stroking)."""

    java_class_name = "com.aspose.python.pdf.operators.EndPath"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

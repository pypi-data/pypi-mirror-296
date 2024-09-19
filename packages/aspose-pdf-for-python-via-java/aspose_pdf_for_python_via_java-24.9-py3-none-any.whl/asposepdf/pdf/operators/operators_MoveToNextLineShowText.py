import jpype 
from asposepdf import Assist 


class operators_MoveToNextLineShowText(Assist.BaseJavaClass):
    """!Class representing ' operator (move to next line and show text)."""

    java_class_name = "com.aspose.python.pdf.operators.MoveToNextLineShowText"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

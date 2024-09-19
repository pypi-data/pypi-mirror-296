import jpype 
from asposepdf import Assist 


class operators_SetWordSpacing(Assist.BaseJavaClass):
    """!Class representing Tw operator (set word spacing)."""

    java_class_name = "com.aspose.python.pdf.operators.SetWordSpacing"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class operators_MoveToNextLine(Assist.BaseJavaClass):
    """!Class representing T* operator (Move to start of the next line)."""

    java_class_name = "com.aspose.python.pdf.operators.MoveToNextLine"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

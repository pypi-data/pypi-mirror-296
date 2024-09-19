import jpype 
from asposepdf import Assist 


class drawing_PatternColorSpace(Assist.BaseJavaClass):
    """!Represents base pattern class."""

    java_class_name = "com.aspose.python.pdf.drawing.PatternColorSpace"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

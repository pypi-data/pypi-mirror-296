import jpype 
from asposepdf import Assist 


class text_SimpleFontSubstitution(Assist.BaseJavaClass):
    """!Represents a class for simple font substitution strategy."""

    java_class_name = "com.aspose.python.pdf.text.SimpleFontSubstitution"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

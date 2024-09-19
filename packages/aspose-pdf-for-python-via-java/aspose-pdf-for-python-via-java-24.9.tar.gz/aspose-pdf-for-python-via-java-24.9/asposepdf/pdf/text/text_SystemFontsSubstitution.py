import jpype 
from asposepdf import Assist 


class text_SystemFontsSubstitution(Assist.BaseJavaClass):
    """!Represents a class for font substitution strategy that substitutes fonts with system fonts."""

    java_class_name = "com.aspose.python.pdf.text.SystemFontsSubstitution"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

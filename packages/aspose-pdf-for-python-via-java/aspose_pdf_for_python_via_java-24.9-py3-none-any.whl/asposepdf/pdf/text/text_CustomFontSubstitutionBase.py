import jpype 
from asposepdf import Assist 


class text_CustomFontSubstitutionBase(Assist.BaseJavaClass):
    """!Represents a base class for custom font substitution strategy."""

    java_class_name = "com.aspose.python.pdf.text.CustomFontSubstitutionBase"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

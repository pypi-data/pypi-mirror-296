import jpype 
from asposepdf import Assist 


class text_FontSubstitution(Assist.BaseJavaClass):
    """!For internal usage only
     Represents a base class for font substitution strategies."""

    java_class_name = "com.aspose.python.pdf.text.FontSubstitution"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

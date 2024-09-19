import jpype 
from asposepdf import Assist 


class operators_SetGlyphsPositionShowText(Assist.BaseJavaClass):
    """!Class representing TJ operator (show text with glyph positioning)."""

    java_class_name = "com.aspose.python.pdf.operators.SetGlyphsPositionShowText"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class operators_GlyphPosition(Assist.BaseJavaClass):
    """!Class describes text and position to use with operator TJ (set glyph with position)"""

    java_class_name = "com.aspose.python.pdf.operators.GlyphPosition"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

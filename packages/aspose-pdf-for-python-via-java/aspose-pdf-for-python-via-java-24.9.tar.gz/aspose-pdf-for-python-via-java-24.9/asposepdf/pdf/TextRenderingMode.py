import jpype 
from asposepdf import Assist 


class TextRenderingMode(Assist.BaseJavaClass):
    """!The text rendering mode, Tmode, determines whether showing text shall cause glyph outlines to be
     stroked, filled, used as a clipping boundary, or some combination of the three."""

    java_class_name = "com.aspose.python.pdf.TextRenderingMode"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _FillThenStrokeTextAndAddPathToClipping = 6
    _FillText = 0
    _StrokeTextAndAddPathToClipping = 5
    _FillThenStrokeText = 2
    _Invisible = 3
    _StrokeText = 1
    _AddPathToClipping = 7
    _FillTextAndAddPathToClipping = 4

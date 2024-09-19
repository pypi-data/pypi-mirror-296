import jpype 
from asposepdf import Assist 


class TextFormattingOptions_LineSpacingMode(Assist.BaseJavaClass):
    """!Defines line spacing specifics"""

    java_class_name = "com.aspose.python.pdf.TextFormattingOptions.LineSpacingMode"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _FontSize = 0
    _FullSize = 1

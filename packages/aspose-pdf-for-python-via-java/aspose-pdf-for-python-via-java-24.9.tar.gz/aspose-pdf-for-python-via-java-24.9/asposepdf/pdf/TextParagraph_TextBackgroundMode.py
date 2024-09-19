import jpype 
from asposepdf import Assist 


class TextParagraph_TextBackgroundMode(Assist.BaseJavaClass):
    """!Background mode for TextParagraph"""

    java_class_name = "com.aspose.python.pdf.TextParagraph.TextBackgroundMode"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _WholeParagraph = 0
    _LogicalLine = 1

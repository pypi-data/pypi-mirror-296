import jpype 
from asposepdf import Assist 


class TextFormattingOptions_WordWrapMode(Assist.BaseJavaClass):
    """!Defines word wrapping strategies"""

    java_class_name = "com.aspose.python.pdf.TextFormattingOptions.WordWrapMode"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _DiscretionaryHyphenation = 1
    _ByWords = 2
    _Undefined = 3
    _NoWrap = 0

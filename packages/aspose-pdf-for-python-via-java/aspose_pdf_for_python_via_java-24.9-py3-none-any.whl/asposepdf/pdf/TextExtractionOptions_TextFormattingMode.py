import jpype 
from asposepdf import Assist 


class TextExtractionOptions_TextFormattingMode(Assist.BaseJavaClass):
    """!Defines different modes which can be used while converting pdf document into text. See
     {@code TextDevice} class."""

    java_class_name = "com.aspose.python.pdf.TextExtractionOptions.TextFormattingMode"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Flatten = 2
    _Raw = 1
    _MemorySaving = 3
    _Pure = 0

import jpype 
from asposepdf import Assist 


class plugins_textextractor_TextExtractorOptions_TextFormattingMode(Assist.BaseJavaClass):
    """!Defines different modes which can be used while converting a PDF document into text. See {@link TextExtractorOptions} class."""

    java_class_name = "com.aspose.python.pdf.plugins.textextractor.TextExtractorOptions.TextFormattingMode"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Plain = 2
    _Raw = 1
    _Pure = 0

import jpype 
from asposepdf import Assist 


class PdfFormatConversionOptions_PuaProcessingStrategy(Assist.BaseJavaClass):
    """!Some PDF documents have special unicode symbols, which are belonged to Private Use Area
     (PUA), see description at https://en.wikipedia.org/wiki/Private_Use_Areas. This symbols cause
     an PDF/A compliant errors like "Text is mapped to Unicode Private Use Area but no ActualText
     entry is present". This enumeration declares a strategies which can be used to handle PUA
     symbols."""

    java_class_name = "com.aspose.python.pdf.PdfFormatConversionOptions.PuaProcessingStrategy"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _SubstitutePuaSymbols = 2
    _SurroundPuaTextWithEmptyActualText = 1
    _None = 0

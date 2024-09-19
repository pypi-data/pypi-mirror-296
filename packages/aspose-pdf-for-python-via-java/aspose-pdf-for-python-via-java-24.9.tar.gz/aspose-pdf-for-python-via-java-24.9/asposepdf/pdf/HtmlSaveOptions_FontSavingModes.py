import jpype 
from asposepdf import Assist 


class HtmlSaveOptions_FontSavingModes(Assist.BaseJavaClass):
    """!Enumerates modes that can be used for saving of fonts referenced in saved PDF."""

    java_class_name = "com.aspose.python.pdf.HtmlSaveOptions.FontSavingModes"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _AlwaysSaveAsTTF = 1
    _AlwaysSaveAsEOT = 2
    _AlwaysSaveAsWOFF = 0
    _DontSave = 4
    _SaveInAllFormats = 3

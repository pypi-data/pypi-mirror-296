import jpype 
from asposepdf import Assist 


class facades_PdfFileEditor_ProgressEventType(Assist.BaseJavaClass):
    """!This enum describes possible progress event types that can occure during concatenation"""

    java_class_name = "com.aspose.python.pdf.facades.PdfFileEditor.ProgressEventType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _DocumentJavaScript = 6
    _AllPagesCopied = 8
    _PageConcatenated = 0
    _DocumentLogicalStructure = 7
    _DocumentEmbeddedFiles = 3
    _DocumentForms = 4
    _BlankPage = 1
    _TotalPercentage = 10
    _DocumentConcated = 9
    _DocumentOutlines = 5

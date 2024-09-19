import jpype 
from asposepdf import Assist 


class facades_PdfFileEditor_ConcatenateCorruptedFileAction(Assist.BaseJavaClass):
    """!Action performed when corrupted file was met in concatenation process."""

    java_class_name = "com.aspose.python.pdf.facades.PdfFileEditor.ConcatenateCorruptedFileAction"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _ConcatenateIgnoringCorrupted = 1
    _ConcatenateIgnoringCorruptedObjects = 2
    _StopWithError = 0

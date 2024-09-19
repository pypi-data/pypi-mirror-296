import jpype 
from asposepdf import Assist 


class facades_PdfFileEditor_ProgressEventHandlerInfo(Assist.BaseJavaClass):
    """!This class represents information about concatenation progress that can be used in external
     application."""

    java_class_name = "com.aspose.python.pdf.facades.PdfFileEditor.ProgressEventHandlerInfo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

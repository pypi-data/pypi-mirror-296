import jpype 
from asposepdf import Assist 


class facades_PdfJavaScriptStripper(Assist.BaseJavaClass):
    """!Class for removing all Java Script code."""

    java_class_name = "com.aspose.python.pdf.facades.PdfJavaScriptStripper"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class facades_PdfFileEditorWeb(Assist.BaseJavaClass):
    """!Represents PdfFileEditorWeb class
     Implements operations with PDF file: concatenation, splitting, extracting pages, making booklet,
     etc."""

    java_class_name = "com.aspose.python.pdf.facades.PdfFileEditorWeb"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class facades_PdfViewer(Assist.BaseJavaClass):
    """!Represents a class to view or print a pdf."""

    java_class_name = "com.aspose.python.pdf.facades.PdfViewer"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)


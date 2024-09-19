import jpype 
from asposepdf import Assist 


class facades_PdfExtractor(Assist.BaseJavaClass):
    """!Class for extracting images and text from PDF document."""

    java_class_name = "com.aspose.python.pdf.facades.PdfExtractor"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

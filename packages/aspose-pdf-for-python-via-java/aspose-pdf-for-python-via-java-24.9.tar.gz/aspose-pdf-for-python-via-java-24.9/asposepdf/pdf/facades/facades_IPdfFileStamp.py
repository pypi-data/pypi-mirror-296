import jpype 
from asposepdf import Assist 


class facades_IPdfFileStamp(Assist.BaseJavaClass):
    """!interface for adding stamps (watermark or background) to PDF files."""

    java_class_name = "com.aspose.python.pdf.facades.IPdfFileStamp"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

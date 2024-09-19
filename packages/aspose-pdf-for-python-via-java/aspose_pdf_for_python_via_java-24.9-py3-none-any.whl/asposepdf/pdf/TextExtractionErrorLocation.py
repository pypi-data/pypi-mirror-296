import jpype 
from asposepdf import Assist 


class TextExtractionErrorLocation(Assist.BaseJavaClass):
    """!Represents the location in the PDF document where text extraction error has appeared."""

    java_class_name = "com.aspose.python.pdf.TextExtractionErrorLocation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

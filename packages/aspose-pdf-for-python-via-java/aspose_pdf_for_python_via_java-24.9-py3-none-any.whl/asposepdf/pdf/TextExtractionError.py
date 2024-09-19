import jpype 
from asposepdf import Assist 


class TextExtractionError(Assist.BaseJavaClass):
    """!Describes the text extraction error has appeared in the PDF document."""

    java_class_name = "com.aspose.python.pdf.TextExtractionError"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

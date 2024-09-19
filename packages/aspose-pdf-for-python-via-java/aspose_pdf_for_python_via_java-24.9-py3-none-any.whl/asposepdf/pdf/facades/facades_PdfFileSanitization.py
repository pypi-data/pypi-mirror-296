import jpype 
from asposepdf import Assist 


class facades_PdfFileSanitization(Assist.BaseJavaClass):
    """!Represents sanitization and recovery API.
     Use it if you can't create/open documents in any other way."""

    java_class_name = "com.aspose.python.pdf.facades.PdfFileSanitization"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

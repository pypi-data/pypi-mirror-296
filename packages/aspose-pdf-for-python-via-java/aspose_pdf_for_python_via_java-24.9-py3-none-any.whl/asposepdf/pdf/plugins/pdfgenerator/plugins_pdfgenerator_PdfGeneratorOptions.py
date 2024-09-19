import jpype 
from asposepdf import Assist 


class plugins_pdfgenerator_PdfGeneratorOptions(Assist.BaseJavaClass):
    """!Represents options for Generator plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.pdfgenerator.PdfGeneratorOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

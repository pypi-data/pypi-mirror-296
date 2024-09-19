import jpype 
from asposepdf import Assist 


class PdfFormatConversionOptions(Assist.BaseJavaClass):
    """!represents set of options for convert PDF document"""

    java_class_name = "com.aspose.python.pdf.PdfFormatConversionOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

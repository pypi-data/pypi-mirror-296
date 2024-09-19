import jpype 
from asposepdf import Assist 


class plugins_pdfa_PdfAOptionsBase(Assist.BaseJavaClass):
    """!Represents the base class for the {@link PdfAConverter} plugin options.
     This class provides properties and methods for configuring the PDF/A conversion and validation process."""

    java_class_name = "com.aspose.python.pdf.plugins.pdfa.PdfAOptionsBase"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

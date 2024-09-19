import jpype 
from asposepdf import Assist 


class PdfFormatConversionOptions_PdfANonSpecificationFlags(Assist.BaseJavaClass):
    """!This class holds flags to control PDF/A conversion for cases when source PDF document doesn't
     correspond to PDF specification. If flags of this clas are used it decreases performance
     but it's necessary when source PDF document can't be convert into PDF/A format by usual way.
     By default all flags are set to false."""

    java_class_name = "com.aspose.python.pdf.PdfFormatConversionOptions.PdfANonSpecificationFlags"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

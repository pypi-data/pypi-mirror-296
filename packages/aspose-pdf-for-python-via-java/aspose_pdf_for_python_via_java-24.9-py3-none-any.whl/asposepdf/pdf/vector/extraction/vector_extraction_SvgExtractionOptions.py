import jpype 
from asposepdf import Assist 


class vector_extraction_SvgExtractionOptions(Assist.BaseJavaClass):
    """!Represents an options class for extracting vector graphics from the pdf document page."""

    java_class_name = "com.aspose.python.pdf.vector.extraction.SvgExtractionOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

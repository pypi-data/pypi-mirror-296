import jpype 
from asposepdf import Assist 


class vector_extraction_SvgExtractor(Assist.BaseJavaClass):
    """!Represents a class to SVG-images extraction from page."""

    java_class_name = "com.aspose.python.pdf.vector.extraction.SvgExtractor"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

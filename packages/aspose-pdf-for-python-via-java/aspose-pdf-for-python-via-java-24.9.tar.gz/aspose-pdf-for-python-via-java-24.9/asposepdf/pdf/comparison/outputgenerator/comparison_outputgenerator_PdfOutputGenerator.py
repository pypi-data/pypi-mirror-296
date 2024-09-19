import jpype 
from asposepdf import Assist 


class comparison_outputgenerator_PdfOutputGenerator(Assist.BaseJavaClass):
    """!Represents a class for generating PDF representation of texts differences."""

    java_class_name = "com.aspose.python.pdf.comparison.outputgenerator.PdfOutputGenerator"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

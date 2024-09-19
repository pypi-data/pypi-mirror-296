import jpype 
from asposepdf import Assist 


class comparison_outputgenerator_HtmlDiffOutputGenerator(Assist.BaseJavaClass):
    """!Represents a class for generating html representation of texts differences.
     Deleted line breaks are indicated by - paragraph mark."""

    java_class_name = "com.aspose.python.pdf.comparison.outputgenerator.HtmlDiffOutputGenerator"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

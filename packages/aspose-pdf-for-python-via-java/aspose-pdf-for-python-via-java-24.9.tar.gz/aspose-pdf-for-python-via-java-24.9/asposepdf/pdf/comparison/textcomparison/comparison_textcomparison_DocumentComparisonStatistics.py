import jpype 
from asposepdf import Assist 


class comparison_textcomparison_DocumentComparisonStatistics(Assist.BaseJavaClass):
    """!Represents a document comparison statistics class."""

    java_class_name = "com.aspose.python.pdf.comparison.textcomparison.DocumentComparisonStatistics"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

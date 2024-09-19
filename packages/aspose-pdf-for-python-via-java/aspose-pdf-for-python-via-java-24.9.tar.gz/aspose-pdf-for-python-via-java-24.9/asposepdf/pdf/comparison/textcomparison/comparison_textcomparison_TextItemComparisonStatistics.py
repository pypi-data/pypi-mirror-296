import jpype 
from asposepdf import Assist 


class comparison_textcomparison_TextItemComparisonStatistics(Assist.BaseJavaClass):
    """!Represents a text comparison ststistics class."""

    java_class_name = "com.aspose.python.pdf.comparison.textcomparison.TextItemComparisonStatistics"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

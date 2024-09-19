import jpype 
from asposepdf import Assist 


class comparison_ComparisonOptions(Assist.BaseJavaClass):
    """!Represents a PDF document comparison options class."""

    java_class_name = "com.aspose.python.pdf.comparison.ComparisonOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

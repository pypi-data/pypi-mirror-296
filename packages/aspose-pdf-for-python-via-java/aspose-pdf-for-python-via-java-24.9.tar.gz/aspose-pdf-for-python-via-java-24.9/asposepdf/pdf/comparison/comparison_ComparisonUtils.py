import jpype 
from asposepdf import Assist 


class comparison_ComparisonUtils(Assist.BaseJavaClass):
    """!Represents a class for comparison utils."""

    java_class_name = "com.aspose.python.pdf.comparison.ComparisonUtils"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

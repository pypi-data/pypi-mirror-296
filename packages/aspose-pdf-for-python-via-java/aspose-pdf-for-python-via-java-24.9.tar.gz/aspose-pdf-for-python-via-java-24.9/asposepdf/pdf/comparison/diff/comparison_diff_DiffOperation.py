import jpype 
from asposepdf import Assist 


class comparison_diff_DiffOperation(Assist.BaseJavaClass):
    """!Represents a class of diff operation."""

    java_class_name = "com.aspose.python.pdf.comparison.diff.DiffOperation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

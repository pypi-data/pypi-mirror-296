import jpype 
from asposepdf import Assist 


class comparison_diff_DiffUtils(Assist.BaseJavaClass):
    """!Represents a utils class for diff algorithm."""

    java_class_name = "com.aspose.python.pdf.comparison.diff.DiffUtils"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

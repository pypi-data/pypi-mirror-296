import jpype 
from asposepdf import Assist 


class comparison_diff_DiffSolver(Assist.BaseJavaClass):
    """!Represents a text difference search algorithm class."""

    java_class_name = "com.aspose.python.pdf.comparison.diff.DiffSolver"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

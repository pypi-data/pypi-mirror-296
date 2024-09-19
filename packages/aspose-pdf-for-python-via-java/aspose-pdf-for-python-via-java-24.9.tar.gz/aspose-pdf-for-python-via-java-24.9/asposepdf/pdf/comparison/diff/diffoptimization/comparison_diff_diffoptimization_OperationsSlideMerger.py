import jpype 
from asposepdf import Assist 


class comparison_diff_diffoptimization_OperationsSlideMerger(Assist.BaseJavaClass):
    """!Represents a class to identifies single edits that are surrounded by equalities
     and merge it with left or right equal operation."""

    java_class_name = "com.aspose.python.pdf.comparison.diff.diffoptimization.OperationsSlideMerger"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

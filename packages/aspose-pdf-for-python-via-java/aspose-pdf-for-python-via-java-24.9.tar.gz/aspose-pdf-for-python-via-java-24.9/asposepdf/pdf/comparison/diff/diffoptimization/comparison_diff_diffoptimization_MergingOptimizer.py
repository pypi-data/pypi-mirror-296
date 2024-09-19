import jpype 
from asposepdf import Assist 


class comparison_diff_diffoptimization_MergingOptimizer(Assist.BaseJavaClass):
    """!Represents class to reorder and merge edit sections.
     It merge equalities and combines adjacent identical changes.
     It sorts and merge changes between Equals operations, because changing their order and merge does not change the result,
     but produces more readable output.
     This combines adjacent Equal operations."""

    java_class_name = "com.aspose.python.pdf.comparison.diff.diffoptimization.MergingOptimizer"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

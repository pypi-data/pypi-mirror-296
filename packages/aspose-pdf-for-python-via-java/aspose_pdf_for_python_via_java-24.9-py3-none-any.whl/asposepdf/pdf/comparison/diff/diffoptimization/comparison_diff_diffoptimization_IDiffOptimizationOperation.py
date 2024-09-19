import jpype 
from asposepdf import Assist 


class comparison_diff_diffoptimization_IDiffOptimizationOperation(Assist.BaseJavaClass):
    """!Represents the interface of difference operations optimizers."""

    java_class_name = "com.aspose.python.pdf.comparison.diff.diffoptimization.IDiffOptimizationOperation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

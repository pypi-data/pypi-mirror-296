import jpype 
from asposepdf import Assist 


class comparison_sidebysidecomparison_SideBySideComparisonOptions(Assist.BaseJavaClass):
    """!Represents an options class for comparing documents with side-by-side output."""

    java_class_name = "com.aspose.python.pdf.comparison.sidebysidecomparison.SideBySideComparisonOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

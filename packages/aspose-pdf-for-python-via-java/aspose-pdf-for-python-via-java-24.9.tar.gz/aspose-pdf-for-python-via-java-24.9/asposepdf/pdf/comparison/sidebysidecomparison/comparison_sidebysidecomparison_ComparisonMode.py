import jpype 
from asposepdf import Assist 


class comparison_sidebysidecomparison_ComparisonMode(Assist.BaseJavaClass):
    """!The comparison mode enumeration."""

    java_class_name = "com.aspose.python.pdf.comparison.sidebysidecomparison.ComparisonMode"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _IgnoreSpaces = 1
    _ParseSpaces = 2
    _Normal = 0

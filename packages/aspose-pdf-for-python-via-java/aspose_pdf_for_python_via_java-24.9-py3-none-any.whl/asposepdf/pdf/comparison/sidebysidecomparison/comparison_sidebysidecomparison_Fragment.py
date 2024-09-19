import jpype 
from asposepdf import Assist 


class comparison_sidebysidecomparison_Fragment(Assist.BaseJavaClass):
    """!Represents text fragment without extra spaces."""

    java_class_name = "com.aspose.python.pdf.comparison.sidebysidecomparison.Fragment"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

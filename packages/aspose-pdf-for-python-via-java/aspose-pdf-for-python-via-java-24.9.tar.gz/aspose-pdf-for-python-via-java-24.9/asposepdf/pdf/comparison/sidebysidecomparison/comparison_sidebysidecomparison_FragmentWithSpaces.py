import jpype 
from asposepdf import Assist 


class comparison_sidebysidecomparison_FragmentWithSpaces(Assist.BaseJavaClass):
    """!Represents text fragments with extra spaces.
     Rect changed to take into account spaces."""

    java_class_name = "com.aspose.python.pdf.comparison.sidebysidecomparison.FragmentWithSpaces"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

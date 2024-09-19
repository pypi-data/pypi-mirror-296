import jpype 
from asposepdf import Assist 


class comparison_sidebysidecomparison_TextFragmentRectanglesComparer(Assist.BaseJavaClass):
    """!Represents a class to compare two Rectangle objects.
     It is used in the context of side-by-side comparison of text fragments in PDF documents."""

    java_class_name = "com.aspose.python.pdf.comparison.sidebysidecomparison.TextFragmentRectanglesComparer"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

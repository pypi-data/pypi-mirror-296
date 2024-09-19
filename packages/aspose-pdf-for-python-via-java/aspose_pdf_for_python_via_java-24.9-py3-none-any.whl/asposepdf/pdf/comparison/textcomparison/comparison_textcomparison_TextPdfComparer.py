import jpype 
from asposepdf import Assist 


class comparison_textcomparison_TextPdfComparer(Assist.BaseJavaClass):
    """!Represents a class to comparison two PDF pages or PDF documents."""

    java_class_name = "com.aspose.python.pdf.comparison.textcomparison.TextPdfComparer"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

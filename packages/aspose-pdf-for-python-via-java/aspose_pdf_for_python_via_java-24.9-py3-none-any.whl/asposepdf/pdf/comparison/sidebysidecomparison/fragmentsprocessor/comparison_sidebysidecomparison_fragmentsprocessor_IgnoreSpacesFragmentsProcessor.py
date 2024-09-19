import jpype 
from asposepdf import Assist 


class comparison_sidebysidecomparison_fragmentsprocessor_IgnoreSpacesFragmentsProcessor(Assist.BaseJavaClass):
    """!Represents a class to process text fragments with ignoring spaces mode.
     This class ignores all whitespace, highlighting individual words as fragments."""

    java_class_name = "com.aspose.python.pdf.comparison.sidebysidecomparison.fragmentsprocessor.IgnoreSpacesFragmentsProcessor"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

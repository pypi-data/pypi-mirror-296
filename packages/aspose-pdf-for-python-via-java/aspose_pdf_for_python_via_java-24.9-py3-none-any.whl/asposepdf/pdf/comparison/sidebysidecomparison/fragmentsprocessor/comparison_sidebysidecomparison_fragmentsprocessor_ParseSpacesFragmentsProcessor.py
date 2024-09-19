import jpype 
from asposepdf import Assist 


class comparison_sidebysidecomparison_fragmentsprocessor_ParseSpacesFragmentsProcessor(Assist.BaseJavaClass):
    """!Represents a class to process text fragments with parse spaces mode.
     This class recognizes spaces between text fragments based on the distance between them."""

    java_class_name = "com.aspose.python.pdf.comparison.sidebysidecomparison.fragmentsprocessor.ParseSpacesFragmentsProcessor"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

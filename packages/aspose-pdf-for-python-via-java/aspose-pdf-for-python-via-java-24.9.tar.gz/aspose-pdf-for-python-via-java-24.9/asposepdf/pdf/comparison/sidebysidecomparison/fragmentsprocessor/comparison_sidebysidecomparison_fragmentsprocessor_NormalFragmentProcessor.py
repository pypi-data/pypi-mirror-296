import jpype 
from asposepdf import Assist 


class comparison_sidebysidecomparison_fragmentsprocessor_NormalFragmentProcessor(Assist.BaseJavaClass):
    """!Represents a class to process text fragments with normal mode.
     This class only considers whitespace within fragments."""

    java_class_name = "com.aspose.python.pdf.comparison.sidebysidecomparison.fragmentsprocessor.NormalFragmentProcessor"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

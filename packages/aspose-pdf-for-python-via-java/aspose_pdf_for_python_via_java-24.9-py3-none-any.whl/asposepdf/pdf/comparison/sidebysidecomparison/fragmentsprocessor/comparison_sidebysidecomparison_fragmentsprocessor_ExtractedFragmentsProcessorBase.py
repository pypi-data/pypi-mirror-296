import jpype 
from asposepdf import Assist 


class comparison_sidebysidecomparison_fragmentsprocessor_ExtractedFragmentsProcessorBase(Assist.BaseJavaClass):
    """!Represents a base class for extracted fragments processors."""

    java_class_name = "com.aspose.python.pdf.comparison.sidebysidecomparison.fragmentsprocessor.ExtractedFragmentsProcessorBase"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

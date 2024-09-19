import jpype 
from asposepdf import Assist 


class comparison_outputgenerator_OutputTextStyle(Assist.BaseJavaClass):
    """!Represents a style set class for marking text changes."""

    java_class_name = "com.aspose.python.pdf.comparison.outputgenerator.OutputTextStyle"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

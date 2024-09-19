import jpype 
from asposepdf import Assist 


class comparison_outputgenerator_TextStyle(Assist.BaseJavaClass):
    """!Represents a text style class."""

    java_class_name = "com.aspose.python.pdf.comparison.outputgenerator.TextStyle"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class markdownoptions_EmphasisStyle(Assist.BaseJavaClass):
    """!Defines the available serialization styles for emphasis and strong emphasis.
     For specification see CommonMark - Emphasis and strong emphasis."""

    java_class_name = "com.aspose.python.pdf.markdownoptions.EmphasisStyle"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Underscore = 1
    _Asterisk = 0

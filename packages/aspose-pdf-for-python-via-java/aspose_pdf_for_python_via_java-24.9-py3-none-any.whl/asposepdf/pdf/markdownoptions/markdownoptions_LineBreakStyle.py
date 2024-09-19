import jpype 
from asposepdf import Assist 


class markdownoptions_LineBreakStyle(Assist.BaseJavaClass):
    """!Represents the possible line break styles for a file."""

    java_class_name = "com.aspose.python.pdf.markdownoptions.LineBreakStyle"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Unix = 1
    _Auto = 2
    _Windows = 0

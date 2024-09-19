import jpype 
from asposepdf import Assist 


class markdownoptions_HeadingStyle(Assist.BaseJavaClass):
    """!Defines the available serialization styles for headings.
     For specification see CommonMark - ATX headings,
     respectively CommonMark - Setext headings."""

    java_class_name = "com.aspose.python.pdf.markdownoptions.HeadingStyle"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Atx = 0
    _Setext = 1

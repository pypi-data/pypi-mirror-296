import jpype 
from asposepdf import Assist 


class markdownoptions_HeadingRecognitionStrategy(Assist.BaseJavaClass):
    """!Represents types of header recognition strategies."""

    java_class_name = "com.aspose.python.pdf.markdownoptions.HeadingRecognitionStrategy"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Auto = 2
    _Outlines = 0
    _None = 3
    _Heuristic = 1

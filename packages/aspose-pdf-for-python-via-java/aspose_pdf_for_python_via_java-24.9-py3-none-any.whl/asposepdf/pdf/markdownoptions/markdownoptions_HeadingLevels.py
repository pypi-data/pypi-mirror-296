import jpype 
from asposepdf import Assist 


class markdownoptions_HeadingLevels(Assist.BaseJavaClass):
    """!Represents a class to work with header levels based on font size."""

    java_class_name = "com.aspose.python.pdf.markdownoptions.HeadingLevels"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

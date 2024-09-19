import jpype 
from asposepdf import Assist 


class CharInfo(Assist.BaseJavaClass):
    """!Represents a character info object. Provides character positioning information."""

    java_class_name = "com.aspose.python.pdf.CharInfo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

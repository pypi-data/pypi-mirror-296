import jpype 
from asposepdf import Assist 


class LevelFormat(Assist.BaseJavaClass):
    """!Represents format of the table of contents."""

    java_class_name = "com.aspose.python.pdf.LevelFormat"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

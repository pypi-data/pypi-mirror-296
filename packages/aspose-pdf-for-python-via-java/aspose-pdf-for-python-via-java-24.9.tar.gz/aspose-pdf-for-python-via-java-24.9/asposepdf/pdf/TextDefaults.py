import jpype 
from asposepdf import Assist 


class TextDefaults(Assist.BaseJavaClass):
    """!Defines text subsystem defaults"""

    java_class_name = "com.aspose.python.pdf.TextDefaults"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

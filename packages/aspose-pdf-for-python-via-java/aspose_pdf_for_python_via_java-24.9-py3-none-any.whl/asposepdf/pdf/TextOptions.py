import jpype 
from asposepdf import Assist 


class TextOptions(Assist.BaseJavaClass):
    """!Represents text processing options"""

    java_class_name = "com.aspose.python.pdf.TextOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

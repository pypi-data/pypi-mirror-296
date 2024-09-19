import jpype 
from asposepdf import Assist 


class TextFormattingOptions(Assist.BaseJavaClass):
    """!Represents text formatting options"""

    java_class_name = "com.aspose.python.pdf.TextFormattingOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

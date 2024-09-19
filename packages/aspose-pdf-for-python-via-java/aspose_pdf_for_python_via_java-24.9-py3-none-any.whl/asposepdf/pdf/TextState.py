import jpype 
from asposepdf import Assist 


class TextState(Assist.BaseJavaClass):
    """!Represents a text state of a text"""

    java_class_name = "com.aspose.python.pdf.TextState"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _TabstopDefaultValue = 8

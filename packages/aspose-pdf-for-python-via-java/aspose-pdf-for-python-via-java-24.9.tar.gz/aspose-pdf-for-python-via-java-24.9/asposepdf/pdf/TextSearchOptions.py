import jpype 
from asposepdf import Assist 


class TextSearchOptions(Assist.BaseJavaClass):
    """!Represents text search options"""

    java_class_name = "com.aspose.python.pdf.TextSearchOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

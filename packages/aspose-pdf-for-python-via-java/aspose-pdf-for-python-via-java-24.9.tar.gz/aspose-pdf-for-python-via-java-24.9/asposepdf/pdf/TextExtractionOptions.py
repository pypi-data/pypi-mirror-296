import jpype 
from asposepdf import Assist 


class TextExtractionOptions(Assist.BaseJavaClass):
    """!Represents text extraction options"""

    java_class_name = "com.aspose.python.pdf.TextExtractionOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

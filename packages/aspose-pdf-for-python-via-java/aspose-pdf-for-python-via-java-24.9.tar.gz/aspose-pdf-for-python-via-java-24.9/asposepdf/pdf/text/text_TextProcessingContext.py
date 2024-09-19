import jpype 
from asposepdf import Assist 


class text_TextProcessingContext(Assist.BaseJavaClass):
    """!Represents text processing context"""

    java_class_name = "com.aspose.python.pdf.text.TextProcessingContext"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

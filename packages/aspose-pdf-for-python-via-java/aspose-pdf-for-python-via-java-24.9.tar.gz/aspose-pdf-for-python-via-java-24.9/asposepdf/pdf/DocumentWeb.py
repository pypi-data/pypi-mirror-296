import jpype 
from asposepdf import Assist 


class DocumentWeb(Assist.BaseJavaClass):
    """!Represents DocumentWeb class"""

    java_class_name = "com.aspose.python.pdf.DocumentWeb"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class Option(Assist.BaseJavaClass):
    """!Class represents option of choice field."""

    java_class_name = "com.aspose.python.pdf.Option"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

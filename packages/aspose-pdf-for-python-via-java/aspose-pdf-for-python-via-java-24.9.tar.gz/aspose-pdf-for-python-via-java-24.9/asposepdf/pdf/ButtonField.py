import jpype 
from asposepdf import Assist 


class ButtonField(Assist.BaseJavaClass):
    """!Class represents push button field."""

    java_class_name = "com.aspose.python.pdf.ButtonField"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

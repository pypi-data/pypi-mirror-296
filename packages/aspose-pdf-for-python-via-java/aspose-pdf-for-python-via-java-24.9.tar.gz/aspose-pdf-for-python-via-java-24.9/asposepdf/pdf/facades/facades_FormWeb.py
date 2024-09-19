import jpype 
from asposepdf import Assist 


class facades_FormWeb(Assist.BaseJavaClass):
    """!Representing Acro form Interface."""

    java_class_name = "com.aspose.python.pdf.facades.FormWeb"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

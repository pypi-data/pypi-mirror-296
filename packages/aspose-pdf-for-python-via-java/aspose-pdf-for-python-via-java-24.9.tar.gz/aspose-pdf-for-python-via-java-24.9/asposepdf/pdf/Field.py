import jpype 
from asposepdf import Assist 


class Field(Assist.BaseJavaClass):
    """!Base class for acro form fields."""

    java_class_name = "com.aspose.python.pdf.Field"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)


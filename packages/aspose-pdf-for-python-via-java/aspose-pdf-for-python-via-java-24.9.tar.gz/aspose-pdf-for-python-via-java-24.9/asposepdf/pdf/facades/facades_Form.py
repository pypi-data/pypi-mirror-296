import jpype 
from asposepdf import Assist 


class facades_Form(Assist.BaseJavaClass):
    """!Class representing Acro form object."""

    java_class_name = "com.aspose.python.pdf.facades.Form"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

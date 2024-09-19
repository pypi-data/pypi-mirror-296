import jpype 
from asposepdf import Assist 


class RegistrationMarkAnnotation(Assist.BaseJavaClass):
    """!Represents a Registration Mark annotation.
     
     Registration marks are symbols added to printing plates or screens to ensure proper alignment of colors during the printing process."""

    java_class_name = "com.aspose.python.pdf.RegistrationMarkAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

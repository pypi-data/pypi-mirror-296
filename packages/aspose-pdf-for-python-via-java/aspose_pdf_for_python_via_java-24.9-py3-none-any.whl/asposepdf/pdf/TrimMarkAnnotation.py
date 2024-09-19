import jpype 
from asposepdf import Assist 


class TrimMarkAnnotation(Assist.BaseJavaClass):
    """!Represents a Trim Mark annotation.
     
     Trim marks are placed at the corners of a printed page to indicate where the page is to be trimmed."""

    java_class_name = "com.aspose.python.pdf.TrimMarkAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

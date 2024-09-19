import jpype 
from asposepdf import Assist 


class BleedMarkAnnotation(Assist.BaseJavaClass):
    """!Represents a Bleed Mark annotation.
     
     Bleed marks are placed at the corners of a printed page to indicate where the page is to be trimmed and how far it is allowed to deviate
     from the trim marks."""

    java_class_name = "com.aspose.python.pdf.BleedMarkAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

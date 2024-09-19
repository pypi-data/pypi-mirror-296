import jpype 
from asposepdf import Assist 


class ElementCollection(Assist.BaseJavaClass):
    """!Collection of base logical structure elements."""

    java_class_name = "com.aspose.python.pdf.ElementCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

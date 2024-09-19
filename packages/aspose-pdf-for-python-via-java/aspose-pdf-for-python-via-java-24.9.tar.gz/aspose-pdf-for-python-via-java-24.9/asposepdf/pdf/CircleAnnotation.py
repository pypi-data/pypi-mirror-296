import jpype 
from asposepdf import Assist 


class CircleAnnotation(Assist.BaseJavaClass):
    """!Class representing Circle annotation."""

    java_class_name = "com.aspose.python.pdf.CircleAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

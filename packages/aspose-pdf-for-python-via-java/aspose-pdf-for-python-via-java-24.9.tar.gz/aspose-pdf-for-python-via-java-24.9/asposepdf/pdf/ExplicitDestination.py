import jpype 
from asposepdf import Assist 


class ExplicitDestination(Assist.BaseJavaClass):
    """!Represents the base class for explicit destinations in PDF document."""

    java_class_name = "com.aspose.python.pdf.ExplicitDestination"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

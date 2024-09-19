import jpype 
from asposepdf import Assist 


class Element(Assist.BaseJavaClass):
    """!Class representing base element of logical structure."""

    java_class_name = "com.aspose.python.pdf.Element"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

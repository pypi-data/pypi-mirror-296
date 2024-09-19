import jpype 
from asposepdf import Assist 


class TabStop(Assist.BaseJavaClass):
    """!Represents a custom Tab stop position in a paragraph."""

    java_class_name = "com.aspose.python.pdf.TabStop"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

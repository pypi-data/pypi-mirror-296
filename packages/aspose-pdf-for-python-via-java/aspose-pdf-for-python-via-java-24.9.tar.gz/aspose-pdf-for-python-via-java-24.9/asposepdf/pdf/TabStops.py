import jpype 
from asposepdf import Assist 


class TabStops(Assist.BaseJavaClass):
    """!Represents a collection of {@code TabStop} objects."""

    java_class_name = "com.aspose.python.pdf.TabStops"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

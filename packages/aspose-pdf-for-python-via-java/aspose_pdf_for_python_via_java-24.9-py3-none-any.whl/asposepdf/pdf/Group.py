import jpype 
from asposepdf import Assist 


class Group(Assist.BaseJavaClass):
    """!A group attributes class specifying the attributes of the page’s page group for use in the
     transparent imaging model."""

    java_class_name = "com.aspose.python.pdf.Group"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

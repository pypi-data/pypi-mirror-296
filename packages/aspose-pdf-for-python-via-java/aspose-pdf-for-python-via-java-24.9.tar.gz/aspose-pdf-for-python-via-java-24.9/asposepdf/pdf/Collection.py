import jpype 
from asposepdf import Assist 


class Collection(Assist.BaseJavaClass):
    """!Represents class for Collection(12.3.5 Collections)."""

    java_class_name = "com.aspose.python.pdf.Collection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

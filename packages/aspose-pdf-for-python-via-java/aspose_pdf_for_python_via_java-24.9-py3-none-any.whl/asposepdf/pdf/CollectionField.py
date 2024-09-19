import jpype 
from asposepdf import Assist 


class CollectionField(Assist.BaseJavaClass):
    """!Represents a document collection schema field class."""

    java_class_name = "com.aspose.python.pdf.CollectionField"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

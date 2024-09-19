import jpype 
from asposepdf import Assist 


class CollectionSchema(Assist.BaseJavaClass):
    """!Represents a class that describes the "Schema" of a document collection."""

    java_class_name = "com.aspose.python.pdf.CollectionSchema"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

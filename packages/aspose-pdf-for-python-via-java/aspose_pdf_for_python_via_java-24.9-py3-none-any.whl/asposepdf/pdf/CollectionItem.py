import jpype 
from asposepdf import Assist 


class CollectionItem(Assist.BaseJavaClass):
    """!Represents a collection item class.
     The collection item contains the data described by the collection schema."""

    java_class_name = "com.aspose.python.pdf.CollectionItem"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

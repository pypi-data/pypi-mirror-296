import jpype 
from asposepdf import Assist 


class CollectionItem_Value(Assist.BaseJavaClass):
    """!Represents a class for a value of collection item."""

    java_class_name = "com.aspose.python.pdf.CollectionItem.Value"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

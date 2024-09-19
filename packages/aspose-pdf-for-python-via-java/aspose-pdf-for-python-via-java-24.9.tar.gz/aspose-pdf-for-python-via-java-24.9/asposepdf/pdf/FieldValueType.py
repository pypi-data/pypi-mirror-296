import jpype 
from asposepdf import Assist 


class FieldValueType(Assist.BaseJavaClass):
    """!Represents the type of a field value in a schema collection."""

    java_class_name = "com.aspose.python.pdf.FieldValueType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Number = 2
    _Text = 1
    _None = 0
    _Date = 3

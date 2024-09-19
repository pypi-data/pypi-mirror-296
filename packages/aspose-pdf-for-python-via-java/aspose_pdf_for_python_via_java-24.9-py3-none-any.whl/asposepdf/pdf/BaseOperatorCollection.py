import jpype 
from asposepdf import Assist 


class BaseOperatorCollection(Assist.BaseJavaClass):
    """!Represents base class for operator collection."""

    java_class_name = "com.aspose.python.pdf.BaseOperatorCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

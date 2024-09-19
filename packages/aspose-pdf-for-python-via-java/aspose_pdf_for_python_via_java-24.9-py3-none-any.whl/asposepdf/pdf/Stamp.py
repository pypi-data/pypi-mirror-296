import jpype 
from asposepdf import Assist 


class Stamp(Assist.BaseJavaClass):
    """!An abstract class for various kinds of stamps which come as descendants."""

    java_class_name = "com.aspose.python.pdf.Stamp"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

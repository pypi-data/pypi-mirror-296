import jpype 
from asposepdf import Assist 


class NamedDestination(Assist.BaseJavaClass):
    """!Instead of being defined directly with the explicit syntax, a destination may be referred to
     indirectly by means of a name object or a byte string."""

    java_class_name = "com.aspose.python.pdf.NamedDestination"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class WarningInfo(Assist.BaseJavaClass):
    """!Immutable object for encapsulating warning information."""

    java_class_name = "com.aspose.python.pdf.WarningInfo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class FloatingBox(Assist.BaseJavaClass):
    """!Represents a FloatingBox in a Pdf document. FloatingBox is custom positioned."""

    java_class_name = "com.aspose.python.pdf.FloatingBox"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

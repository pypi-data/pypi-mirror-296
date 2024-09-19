import jpype 
from asposepdf import Assist 


class HideAction(Assist.BaseJavaClass):
    """!Represents a hide action that hides or shows one or more annotations on the screen by setting or clearing their Hidden flags."""

    java_class_name = "com.aspose.python.pdf.HideAction"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

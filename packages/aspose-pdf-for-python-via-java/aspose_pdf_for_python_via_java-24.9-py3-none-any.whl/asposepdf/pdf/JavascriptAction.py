import jpype 
from asposepdf import Assist 


class JavascriptAction(Assist.BaseJavaClass):
    """!Class representing javascript action."""

    java_class_name = "com.aspose.python.pdf.JavascriptAction"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

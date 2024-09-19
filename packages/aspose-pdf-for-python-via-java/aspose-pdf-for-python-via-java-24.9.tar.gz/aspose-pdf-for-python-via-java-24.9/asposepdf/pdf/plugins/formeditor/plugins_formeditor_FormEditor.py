import jpype 
from asposepdf import Assist 


class plugins_formeditor_FormEditor(Assist.BaseJavaClass):
    """!Represents FormEditor plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.formeditor.FormEditor"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

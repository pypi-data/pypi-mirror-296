import jpype 
from asposepdf import Assist 


class plugins_formeditor_FormFieldSetOptions(Assist.BaseJavaClass):
    """!Represents options for set properties in Field."""

    java_class_name = "com.aspose.python.pdf.plugins.formeditor.FormFieldSetOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

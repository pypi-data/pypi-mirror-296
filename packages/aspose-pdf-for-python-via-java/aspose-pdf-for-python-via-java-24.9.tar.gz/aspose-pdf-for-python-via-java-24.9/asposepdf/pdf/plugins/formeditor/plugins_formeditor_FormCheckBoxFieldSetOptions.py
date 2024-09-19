import jpype 
from asposepdf import Assist 


class plugins_formeditor_FormCheckBoxFieldSetOptions(Assist.BaseJavaClass):
    """!Represents options for set properties in CheckboxField."""

    java_class_name = "com.aspose.python.pdf.plugins.formeditor.FormCheckBoxFieldSetOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

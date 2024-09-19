import jpype 
from asposepdf import Assist 


class plugins_formeditor_FormComboBoxFieldSetOptions(Assist.BaseJavaClass):
    """!Represents options for set properties in ComboBoxField."""

    java_class_name = "com.aspose.python.pdf.plugins.formeditor.FormComboBoxFieldSetOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

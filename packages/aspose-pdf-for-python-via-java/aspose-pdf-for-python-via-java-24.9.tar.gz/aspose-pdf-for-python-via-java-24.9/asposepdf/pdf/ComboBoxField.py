import jpype 
from asposepdf import Assist 


class ComboBoxField(Assist.BaseJavaClass):
    """!Class representing Combobox field of the form."""

    java_class_name = "com.aspose.python.pdf.ComboBoxField"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

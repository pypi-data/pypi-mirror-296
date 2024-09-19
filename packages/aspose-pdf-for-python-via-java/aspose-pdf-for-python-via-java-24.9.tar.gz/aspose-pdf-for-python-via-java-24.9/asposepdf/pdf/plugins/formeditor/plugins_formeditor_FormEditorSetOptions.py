import jpype 
from asposepdf import Assist 


class plugins_formeditor_FormEditorSetOptions(Assist.BaseJavaClass):
    """!Represents options for set fields (not annotations) properties."""

    java_class_name = "com.aspose.python.pdf.plugins.formeditor.FormEditorSetOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

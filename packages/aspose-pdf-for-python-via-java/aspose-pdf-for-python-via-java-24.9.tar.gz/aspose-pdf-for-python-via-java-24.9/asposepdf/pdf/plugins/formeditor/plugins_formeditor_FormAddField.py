import jpype 
from asposepdf import Assist 


class plugins_formeditor_FormAddField(Assist.BaseJavaClass):
    """!Class for adding field (by using AddField method) to the document, according to the gived FormFieldCreateOptions descendant."""

    java_class_name = "com.aspose.python.pdf.plugins.formeditor.FormAddField"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

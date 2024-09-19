import jpype 
from asposepdf import Assist 


class facades_FormEditor(Assist.BaseJavaClass):
    """!Class for editing forms (adding/deleting field etc)"""

    java_class_name = "com.aspose.python.pdf.facades.FormEditor"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

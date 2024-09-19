import jpype 
from asposepdf import Assist 


class facades_IFormEditor(Assist.BaseJavaClass):
    """!Class for editing forms (adding/deleting field etc)"""

    java_class_name = "com.aspose.python.pdf.facades.IFormEditor"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

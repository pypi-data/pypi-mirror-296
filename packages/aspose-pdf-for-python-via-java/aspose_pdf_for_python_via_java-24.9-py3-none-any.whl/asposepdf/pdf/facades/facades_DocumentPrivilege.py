import jpype 
from asposepdf import Assist 


class facades_DocumentPrivilege(Assist.BaseJavaClass):
    java_class_name = "com.aspose.python.pdf.facades.DocumentPrivilege"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

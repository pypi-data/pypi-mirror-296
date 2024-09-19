import jpype 
from asposepdf import Assist 


class Id(Assist.BaseJavaClass):
    java_class_name = "com.aspose.python.pdf.Id"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

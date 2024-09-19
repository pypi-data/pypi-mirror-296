import jpype 
from asposepdf import Assist 


class StampAnnotation(Assist.BaseJavaClass):
    java_class_name = "com.aspose.python.pdf.StampAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

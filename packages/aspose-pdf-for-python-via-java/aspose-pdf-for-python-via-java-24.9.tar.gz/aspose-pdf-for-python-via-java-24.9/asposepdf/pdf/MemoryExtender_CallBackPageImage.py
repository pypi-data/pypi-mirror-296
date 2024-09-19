import jpype 
from asposepdf import Assist 


class MemoryExtender_CallBackPageImage(Assist.BaseJavaClass):
    """!The call back procedure for manipulating the cache."""

    java_class_name = "com.aspose.python.pdf.MemoryExtender.CallBackPageImage"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

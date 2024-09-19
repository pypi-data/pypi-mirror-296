import jpype 
from asposepdf import Assist 


class MemoryExtender(Assist.BaseJavaClass):
    """!Represents MemoryExtender class Using large files on a system with limited heap memory, can be
     enabled to use disk space as a temporary swap memory."""

    java_class_name = "com.aspose.python.pdf.MemoryExtender"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class multithreading_IInterruptMonitor(Assist.BaseJavaClass):
    """!Represents information about interruption."""

    java_class_name = "com.aspose.python.pdf.multithreading.IInterruptMonitor"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

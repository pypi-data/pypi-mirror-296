import jpype 
from asposepdf import Assist 


class MemoryCleaner(Assist.BaseJavaClass):
    """!Represents MemoryCleaner class"""

    java_class_name = "com.aspose.python.pdf.MemoryCleaner"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

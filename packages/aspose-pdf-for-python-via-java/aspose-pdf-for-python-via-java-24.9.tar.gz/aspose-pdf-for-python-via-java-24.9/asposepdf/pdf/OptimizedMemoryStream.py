import jpype 
from asposepdf import Assist 


class OptimizedMemoryStream(Assist.BaseJavaClass):
    """!Defines a MemoryStream that can contains more standard capacity"""

    java_class_name = "com.aspose.python.pdf.OptimizedMemoryStream"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _DefaultBufferSize = 1000000

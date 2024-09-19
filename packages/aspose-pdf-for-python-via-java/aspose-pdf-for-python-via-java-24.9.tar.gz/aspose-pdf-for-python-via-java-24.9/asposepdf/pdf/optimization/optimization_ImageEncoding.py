import jpype 
from asposepdf import Assist 


class optimization_ImageEncoding(Assist.BaseJavaClass):
    """!Image encoding types."""

    java_class_name = "com.aspose.python.pdf.optimization.ImageEncoding"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Flate = 2
    _Jpeg = 1
    _Jpeg2000 = 3
    _Unchanged = 0

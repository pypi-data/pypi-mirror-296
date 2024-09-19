import jpype 
from asposepdf import Assist 


class optimization_ImageCompressionVersion(Assist.BaseJavaClass):
    """!Describes versions of image compression algorithm."""

    java_class_name = "com.aspose.python.pdf.optimization.ImageCompressionVersion"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Mixed = 3
    _Standard = 0
    _Fast = 2

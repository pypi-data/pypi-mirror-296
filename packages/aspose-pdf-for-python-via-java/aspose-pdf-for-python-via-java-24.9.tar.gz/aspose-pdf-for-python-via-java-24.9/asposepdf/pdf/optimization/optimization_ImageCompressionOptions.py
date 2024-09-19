import jpype 
from asposepdf import Assist 


class optimization_ImageCompressionOptions(Assist.BaseJavaClass):
    """!Class contains set  options for image compression."""

    java_class_name = "com.aspose.python.pdf.optimization.ImageCompressionOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

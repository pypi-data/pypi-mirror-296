import jpype 
from asposepdf import Assist 


class WatermarkAnnotation(Assist.BaseJavaClass):
    """!Class describes Watermark annotation object."""

    java_class_name = "com.aspose.python.pdf.WatermarkAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

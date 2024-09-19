import jpype 
from asposepdf import Assist 


class RichMediaAnnotation(Assist.BaseJavaClass):
    """!Class describes RichMediaAnnotation which allows embed video/audio data into PDF document."""

    java_class_name = "com.aspose.python.pdf.RichMediaAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

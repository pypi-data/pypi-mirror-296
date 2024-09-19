import jpype 
from asposepdf import Assist 


class ScreenAnnotation(Assist.BaseJavaClass):
    """!A screen annotation that specifies a region of a page upon which media clips may be played."""

    java_class_name = "com.aspose.python.pdf.ScreenAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

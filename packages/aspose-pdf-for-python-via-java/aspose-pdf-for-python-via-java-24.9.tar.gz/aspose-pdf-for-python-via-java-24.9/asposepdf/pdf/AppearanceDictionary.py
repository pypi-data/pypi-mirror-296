import jpype 
from asposepdf import Assist 


class AppearanceDictionary(Assist.BaseJavaClass):
    """!Annotation appearance dictionary specifying how the annotation shall be presented visually on the
     page."""

    java_class_name = "com.aspose.python.pdf.AppearanceDictionary"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

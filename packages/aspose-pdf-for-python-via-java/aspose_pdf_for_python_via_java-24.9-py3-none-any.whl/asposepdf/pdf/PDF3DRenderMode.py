import jpype 
from asposepdf import Assist 


class PDF3DRenderMode(Assist.BaseJavaClass):
    """!Class PDF3DRenderMode."""

    java_class_name = "com.aspose.python.pdf.PDF3DRenderMode"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)


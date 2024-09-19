import jpype 
from asposepdf import Assist 


class PDF3DCuttingPlaneOrientation(Assist.BaseJavaClass):
    """!Class PDF3DCuttingPlaneOrientation."""

    java_class_name = "com.aspose.python.pdf.PDF3DCuttingPlaneOrientation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

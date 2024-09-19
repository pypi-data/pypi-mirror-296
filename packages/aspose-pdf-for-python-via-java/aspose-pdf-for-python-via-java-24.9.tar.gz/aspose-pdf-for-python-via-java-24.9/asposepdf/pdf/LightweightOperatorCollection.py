import jpype 
from asposepdf import Assist 


class LightweightOperatorCollection(Assist.BaseJavaClass):
    """!Lightweight operator collection. Intended to be used in scenarios when underlying contents stream
     is not attached, where just operator collection is required as a result."""

    java_class_name = "com.aspose.python.pdf.LightweightOperatorCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class RichMediaAnnotation_ActivationEvent(Assist.BaseJavaClass):
    """!Event which activates annotation."""

    java_class_name = "com.aspose.python.pdf.RichMediaAnnotation.ActivationEvent"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _PageVisible = 2
    _Click = 0
    _PageOpen = 1

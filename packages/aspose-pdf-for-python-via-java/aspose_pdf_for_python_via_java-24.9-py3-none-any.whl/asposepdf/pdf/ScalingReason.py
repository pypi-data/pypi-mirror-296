import jpype 
from asposepdf import Assist 


class ScalingReason(Assist.BaseJavaClass):
    """!The circumstances under which the icon shall be scaled inside the annotation rectangle."""

    java_class_name = "com.aspose.python.pdf.ScalingReason"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _IconIsSmaller = 2
    _IconIsBigger = 1
    _Never = 3
    _Always = 0

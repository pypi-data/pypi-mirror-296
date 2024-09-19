import jpype 
from asposepdf import Assist 


class RenditionOperation(Assist.BaseJavaClass):
    """!The operation to perform when the action is triggered."""

    java_class_name = "com.aspose.python.pdf.RenditionOperation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Undefined = -1
    _PlayStop = 0
    _Pause = 2
    _Stop = 1
    _PlayResume = 4
    _Resume = 3

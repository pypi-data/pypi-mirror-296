import jpype 
from asposepdf import Assist 


class devices_FormPresentationMode(Assist.BaseJavaClass):
    """!Used to specify the form presentation mode when printing or converting to image pdf documents."""

    java_class_name = "com.aspose.python.pdf.devices.FormPresentationMode"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Production = 0
    _Editor = 1

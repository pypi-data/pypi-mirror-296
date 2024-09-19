import jpype 
from asposepdf import Assist 


class ofd_converters_DocBodyConverter(Assist.BaseJavaClass):
    """!Document body converter."""

    java_class_name = "com.aspose.python.pdf.ofd.converters.DocBodyConverter"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

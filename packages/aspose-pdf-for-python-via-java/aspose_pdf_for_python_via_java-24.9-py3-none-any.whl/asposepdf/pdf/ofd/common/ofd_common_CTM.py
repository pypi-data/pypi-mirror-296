import jpype 
from asposepdf import Assist 


class ofd_common_CTM(Assist.BaseJavaClass):
    """!CTM transformation."""

    java_class_name = "com.aspose.python.pdf.ofd.common.CTM"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

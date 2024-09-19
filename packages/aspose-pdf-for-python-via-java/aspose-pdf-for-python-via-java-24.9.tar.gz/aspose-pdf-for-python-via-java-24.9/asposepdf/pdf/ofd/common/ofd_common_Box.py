import jpype 
from asposepdf import Assist 


class ofd_common_Box(Assist.BaseJavaClass):
    """!Class represents bounding box."""

    java_class_name = "com.aspose.python.pdf.ofd.common.Box"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

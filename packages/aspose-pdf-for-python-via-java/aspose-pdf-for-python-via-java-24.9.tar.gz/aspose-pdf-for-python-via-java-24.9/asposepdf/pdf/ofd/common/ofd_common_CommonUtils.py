import jpype 
from asposepdf import Assist 


class ofd_common_CommonUtils(Assist.BaseJavaClass):
    """!Class with utility functions."""

    java_class_name = "com.aspose.python.pdf.ofd.common.CommonUtils"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

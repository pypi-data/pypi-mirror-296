import jpype 
from asposepdf import Assist 


class DefaultDirectory(Assist.BaseJavaClass):
    """!Specifies default path for some purpose"""

    java_class_name = "com.aspose.python.pdf.DefaultDirectory"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class exceptions_CorruptContentException(Assist.BaseJavaClass):
    """!Represents CorruptContentException class"""

    java_class_name = "com.aspose.python.pdf.exceptions.CorruptContentException"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

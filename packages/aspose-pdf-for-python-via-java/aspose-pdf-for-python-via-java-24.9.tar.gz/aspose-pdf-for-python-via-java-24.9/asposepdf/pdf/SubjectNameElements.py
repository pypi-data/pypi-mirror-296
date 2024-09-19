import jpype 
from asposepdf import Assist 


class SubjectNameElements(Assist.BaseJavaClass):
    """!Enumeration describes elements in signature subject string."""

    java_class_name = "com.aspose.python.pdf.SubjectNameElements"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _S = 4
    _C = 5
    _E = 6
    _OU = 3
    _CN = 0
    _L = 2
    _O = 1

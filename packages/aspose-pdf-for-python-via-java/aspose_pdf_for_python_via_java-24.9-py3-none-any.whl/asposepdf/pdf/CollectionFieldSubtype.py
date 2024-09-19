import jpype 
from asposepdf import Assist 


class CollectionFieldSubtype(Assist.BaseJavaClass):
    """!Represents the subtype parameter of a field in a sceme collection."""

    java_class_name = "com.aspose.python.pdf.CollectionFieldSubtype"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Desc = 5
    _CreationDate = 7
    _S = 1
    _D = 2
    _CompressedSize = 9
    _F = 4
    _Size = 8
    _ModDate = 6
    _None = 0
    _N = 3

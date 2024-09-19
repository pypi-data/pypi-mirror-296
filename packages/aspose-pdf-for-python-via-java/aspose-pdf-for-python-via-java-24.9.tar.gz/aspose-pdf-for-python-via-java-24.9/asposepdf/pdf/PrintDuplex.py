import jpype 
from asposepdf import Assist 


class PrintDuplex(Assist.BaseJavaClass):
    """!The paper handling option to use when printing the file from the print dialog.."""

    java_class_name = "com.aspose.python.pdf.PrintDuplex"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Simplex = 0
    _DuplexFlipShortEdge = 1
    _DuplexFlipLongEdge = 2

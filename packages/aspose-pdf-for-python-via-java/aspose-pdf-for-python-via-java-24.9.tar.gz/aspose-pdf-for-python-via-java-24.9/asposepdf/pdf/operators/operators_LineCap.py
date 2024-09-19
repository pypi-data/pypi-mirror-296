import jpype 
from asposepdf import Assist 


class operators_LineCap(Assist.BaseJavaClass):
    """!The line cap style shall specify the shape that shall be used at the ends of open subpaths (and dashes, if any) when they are stroked."""

    java_class_name = "com.aspose.python.pdf.operators.LineCap"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _RoundCap = 1
    _ButtCap = 0
    _SquareCap = 2

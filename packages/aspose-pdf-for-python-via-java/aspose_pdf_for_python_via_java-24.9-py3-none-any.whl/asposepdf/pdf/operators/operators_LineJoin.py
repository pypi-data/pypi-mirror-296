import jpype 
from asposepdf import Assist 


class operators_LineJoin(Assist.BaseJavaClass):
    """!The line join style shall specify the shape to be used at the corners of paths that are stroked."""

    java_class_name = "com.aspose.python.pdf.operators.LineJoin"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _RoundJoin = 1
    _MiterJoin = 0
    _BevelJoin = 2

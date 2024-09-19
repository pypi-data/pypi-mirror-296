import jpype 
from asposepdf import Assist 


class operators_SetLineJoin(Assist.BaseJavaClass):
    """!Class representing j operator (set line join style).
     
     @see LineJoin"""

    java_class_name = "com.aspose.python.pdf.operators.SetLineJoin"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

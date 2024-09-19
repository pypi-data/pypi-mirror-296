import jpype 
from asposepdf import Assist 


class OperatorCollection(Assist.BaseJavaClass):
    """!Class represents collection of operators"""

    java_class_name = "com.aspose.python.pdf.OperatorCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

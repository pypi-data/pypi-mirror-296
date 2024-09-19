import jpype 
from asposepdf import Assist 


class operators_BasicSetColorOperator(Assist.BaseJavaClass):
    """!Base class for set color operators."""

    java_class_name = "com.aspose.python.pdf.operators.BasicSetColorOperator"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

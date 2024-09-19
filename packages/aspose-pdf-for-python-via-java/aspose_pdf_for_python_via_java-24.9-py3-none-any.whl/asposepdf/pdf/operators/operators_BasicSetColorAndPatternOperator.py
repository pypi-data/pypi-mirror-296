import jpype 
from asposepdf import Assist 


class operators_BasicSetColorAndPatternOperator(Assist.BaseJavaClass):
    """!Base operator for all Set Color operators."""

    java_class_name = "com.aspose.python.pdf.operators.BasicSetColorAndPatternOperator"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

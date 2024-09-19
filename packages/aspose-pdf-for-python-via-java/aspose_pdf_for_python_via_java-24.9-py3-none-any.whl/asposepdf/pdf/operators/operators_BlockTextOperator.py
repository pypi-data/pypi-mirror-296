import jpype 
from asposepdf import Assist 


class operators_BlockTextOperator(Assist.BaseJavaClass):
    """!Abstract base class for text block operators i.e. Begin and End text operators (BT/ET)"""

    java_class_name = "com.aspose.python.pdf.operators.BlockTextOperator"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

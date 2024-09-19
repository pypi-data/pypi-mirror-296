import jpype 
from asposepdf import Assist 


class operators_Do(Assist.BaseJavaClass):
    """!Class representing Do operator (Invoke XObject)."""

    java_class_name = "com.aspose.python.pdf.operators.Do"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

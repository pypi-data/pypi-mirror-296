import jpype 
from asposepdf import Assist 


class CheckboxField(Assist.BaseJavaClass):
    """!Class representing checkbox field"""

    java_class_name = "com.aspose.python.pdf.CheckboxField"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

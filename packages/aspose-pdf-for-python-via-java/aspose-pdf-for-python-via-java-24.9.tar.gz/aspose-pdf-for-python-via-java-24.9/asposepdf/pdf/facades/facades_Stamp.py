import jpype 
from asposepdf import Assist 


class facades_Stamp(Assist.BaseJavaClass):
    """!Class represeting stamp."""

    java_class_name = "com.aspose.python.pdf.facades.Stamp"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

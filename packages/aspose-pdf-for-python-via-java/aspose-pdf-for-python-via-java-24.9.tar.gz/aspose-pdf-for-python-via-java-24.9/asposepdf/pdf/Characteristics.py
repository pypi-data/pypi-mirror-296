import jpype 
from asposepdf import Assist 


class Characteristics(Assist.BaseJavaClass):
    """!Represents annotation characteristics"""

    java_class_name = "com.aspose.python.pdf.Characteristics"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class SaveOptions_BorderPartStyle(Assist.BaseJavaClass):
    """!Represents information of one part of border(top, bottom, left side or right side)"""

    java_class_name = "com.aspose.python.pdf.SaveOptions.BorderPartStyle"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

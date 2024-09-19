import jpype 
from asposepdf import Assist 


class SaveOptions_MarginPartStyle(Assist.BaseJavaClass):
    """!Represents information of one part of margin(top, botom, left side or right side)"""

    java_class_name = "com.aspose.python.pdf.SaveOptions.MarginPartStyle"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

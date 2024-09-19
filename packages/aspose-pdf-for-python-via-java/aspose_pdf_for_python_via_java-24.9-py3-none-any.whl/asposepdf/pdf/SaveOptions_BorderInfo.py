import jpype 
from asposepdf import Assist 


class SaveOptions_BorderInfo(Assist.BaseJavaClass):
    """!Instance of this class represents information about border That can be drown on some result
     document."""

    java_class_name = "com.aspose.python.pdf.SaveOptions.BorderInfo"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

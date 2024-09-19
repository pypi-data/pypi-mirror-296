import jpype 
from asposepdf import Assist 


class TabLeaderType(Assist.BaseJavaClass):
    """!Enumerates the tab leader types."""

    java_class_name = "com.aspose.python.pdf.TabLeaderType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Dash = 1
    _Dot = 2
    _None = 3
    _Solid = 0

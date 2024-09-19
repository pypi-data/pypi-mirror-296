import jpype 
from asposepdf import Assist 


class TabAlignmentType(Assist.BaseJavaClass):
    """!Enumerates the tab alignment types."""

    java_class_name = "com.aspose.python.pdf.TabAlignmentType"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _Center = 1
    _Left = 0
    _Right = 2

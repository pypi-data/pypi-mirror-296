import jpype 
from asposepdf import Assist 


class LineEndingsDrawer(Assist.BaseJavaClass):
    """!Draws line endings for annotations. Internal class for internal usage only."""

    java_class_name = "com.aspose.python.pdf.LineEndingsDrawer"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class drawing_Path(Assist.BaseJavaClass):
    """!Represents arc."""

    java_class_name = "com.aspose.python.pdf.drawing.Path"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

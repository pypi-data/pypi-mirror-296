import jpype 
from asposepdf import Assist 


class IconFit(Assist.BaseJavaClass):
    """!Describes how the widget annotation's icon shall be displayed within its annotation rectangle."""

    java_class_name = "com.aspose.python.pdf.IconFit"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

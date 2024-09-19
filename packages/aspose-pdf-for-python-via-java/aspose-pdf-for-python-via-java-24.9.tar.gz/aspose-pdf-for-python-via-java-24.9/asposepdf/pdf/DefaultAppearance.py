import jpype 
from asposepdf import Assist 


class DefaultAppearance(Assist.BaseJavaClass):
    """!Describes default appearance of field (font, text size and color)."""

    java_class_name = "com.aspose.python.pdf.DefaultAppearance"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class facades_FormattedText(Assist.BaseJavaClass):
    """!Class which represents formatted text. Contains information about text and its color, size,
     style."""

    java_class_name = "com.aspose.python.pdf.facades.FormattedText"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

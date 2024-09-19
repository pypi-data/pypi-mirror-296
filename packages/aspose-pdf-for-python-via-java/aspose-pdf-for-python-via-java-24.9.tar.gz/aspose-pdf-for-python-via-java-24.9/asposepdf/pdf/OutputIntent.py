import jpype 
from asposepdf import Assist 


class OutputIntent(Assist.BaseJavaClass):
    """!Represents an output intent that matches the color characteristics of a PDF document with those
     of a target output device or production environment in which the document will be printed."""

    java_class_name = "com.aspose.python.pdf.OutputIntent"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

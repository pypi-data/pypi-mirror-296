import jpype 
from asposepdf import Assist 


class CommonFigureAnnotation(Assist.BaseJavaClass):
    """!Abstract class representing common figure annotation."""

    java_class_name = "com.aspose.python.pdf.CommonFigureAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

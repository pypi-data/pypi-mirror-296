import jpype 
from asposepdf import Assist 


class FigureElement(Assist.BaseJavaClass):
    """!Class representing logical structure figure."""

    java_class_name = "com.aspose.python.pdf.FigureElement"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

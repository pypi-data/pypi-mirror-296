import jpype 
from asposepdf import Assist 


class TeXFragment(Assist.BaseJavaClass):
    """!Represents LaTeX fragment."""

    java_class_name = "com.aspose.python.pdf.TeXFragment"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

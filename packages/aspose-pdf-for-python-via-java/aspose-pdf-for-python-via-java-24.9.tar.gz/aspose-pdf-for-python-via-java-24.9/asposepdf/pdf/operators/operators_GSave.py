import jpype 
from asposepdf import Assist 


class operators_GSave(Assist.BaseJavaClass):
    """!Class representing q operator (save graphics state)."""

    java_class_name = "com.aspose.python.pdf.operators.GSave"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

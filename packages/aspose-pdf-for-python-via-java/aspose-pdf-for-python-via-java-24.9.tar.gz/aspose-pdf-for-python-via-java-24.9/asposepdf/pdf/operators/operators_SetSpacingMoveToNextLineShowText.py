import jpype 
from asposepdf import Assist 


class operators_SetSpacingMoveToNextLineShowText(Assist.BaseJavaClass):
    """!Class representing " operator (set word and character spacing, move to the next line and show
     text)."""

    java_class_name = "com.aspose.python.pdf.operators.SetSpacingMoveToNextLineShowText"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

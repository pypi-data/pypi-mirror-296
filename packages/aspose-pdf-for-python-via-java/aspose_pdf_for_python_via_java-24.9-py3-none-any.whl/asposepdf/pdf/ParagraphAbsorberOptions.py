import jpype 
from asposepdf import Assist 


class ParagraphAbsorberOptions(Assist.BaseJavaClass):
    """!Represents options for the {@link ParagraphAbsorber}."""

    java_class_name = "com.aspose.python.pdf.ParagraphAbsorberOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

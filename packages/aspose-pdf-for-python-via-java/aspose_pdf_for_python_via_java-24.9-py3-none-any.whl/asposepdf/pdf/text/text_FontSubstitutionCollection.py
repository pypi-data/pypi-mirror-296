import jpype 
from asposepdf import Assist 


class text_FontSubstitutionCollection(Assist.BaseJavaClass):
    """!Represents font substitution strategies collection."""

    java_class_name = "com.aspose.python.pdf.text.FontSubstitutionCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

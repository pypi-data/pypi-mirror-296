import jpype 
from asposepdf import Assist 


class tagged_logicalstructure_AttributeKey(Assist.BaseJavaClass):
    """!Represents Standard Attribute Keys."""

    java_class_name = "com.aspose.python.pdf.tagged.logicalstructure.AttributeKey"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)


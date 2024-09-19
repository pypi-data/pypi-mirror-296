import jpype 
from asposepdf import Assist 


class tagged_logicalstructure_ElementList(Assist.BaseJavaClass):
    """!Represents an ordered collection of elements."""

    java_class_name = "com.aspose.python.pdf.tagged.logicalstructure.ElementList"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

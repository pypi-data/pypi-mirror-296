import jpype 
from asposepdf import Assist 


class tagged_logicalstructure_StructureAttributes(Assist.BaseJavaClass):
    """!Represents attributes of structure element for standard attribute owners."""

    java_class_name = "com.aspose.python.pdf.tagged.logicalstructure.StructureAttributes"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class tagged_logicalstructure_StructTreeRootElement(Assist.BaseJavaClass):
    """!Represents StructTreeRoot object in logical structure."""

    java_class_name = "com.aspose.python.pdf.tagged.logicalstructure.StructTreeRootElement"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

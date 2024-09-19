import jpype 
from asposepdf import Assist 


class tagged_logicalstructure_elements_ils_WarichuWTElement(Assist.BaseJavaClass):
    """!Represents WT structure element in logical structure of the Warichu."""

    java_class_name = "com.aspose.python.pdf.tagged.logicalstructure.elements.ils.WarichuWTElement"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

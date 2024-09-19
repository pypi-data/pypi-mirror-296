import jpype 
from asposepdf import Assist 


class tagged_logicalstructure_elements_bls_BLSElement(Assist.BaseJavaClass):
    """!Represents a base class for block-level structure elements in logical structure."""

    java_class_name = "com.aspose.python.pdf.tagged.logicalstructure.elements.bls.BLSElement"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

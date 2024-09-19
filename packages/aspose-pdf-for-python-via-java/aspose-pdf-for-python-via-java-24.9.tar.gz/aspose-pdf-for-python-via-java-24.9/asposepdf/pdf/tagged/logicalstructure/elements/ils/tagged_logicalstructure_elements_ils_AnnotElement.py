import jpype 
from asposepdf import Assist 


class tagged_logicalstructure_elements_ils_AnnotElement(Assist.BaseJavaClass):
    """!Represents Annot structure element in logical structure."""

    java_class_name = "com.aspose.python.pdf.tagged.logicalstructure.elements.ils.AnnotElement"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class tagged_logicalstructure_elements_bls_TableTFootElement(Assist.BaseJavaClass):
    """!Represents TFoot structure element in logical structure of the table."""

    java_class_name = "com.aspose.python.pdf.tagged.logicalstructure.elements.bls.TableTFootElement"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class tagged_logicalstructure_elements_bls_TableTRElement(Assist.BaseJavaClass):
    """!Represents TR structure element in logical structure of the table."""

    java_class_name = "com.aspose.python.pdf.tagged.logicalstructure.elements.bls.TableTRElement"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

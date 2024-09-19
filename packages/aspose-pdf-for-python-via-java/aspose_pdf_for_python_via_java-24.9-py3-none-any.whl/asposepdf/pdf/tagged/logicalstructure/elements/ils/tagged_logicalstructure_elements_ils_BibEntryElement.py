import jpype 
from asposepdf import Assist 


class tagged_logicalstructure_elements_ils_BibEntryElement(Assist.BaseJavaClass):
    """!Represents BibEntry structure element in logical structure."""

    java_class_name = "com.aspose.python.pdf.tagged.logicalstructure.elements.ils.BibEntryElement"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

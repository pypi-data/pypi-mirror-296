import jpype 
from asposepdf import Assist 


class tagged_logicalstructure_elements_ITextElement(Assist.BaseJavaClass):
    """!Interface for presenting text structure elements."""

    java_class_name = "com.aspose.python.pdf.tagged.logicalstructure.elements.ITextElement"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

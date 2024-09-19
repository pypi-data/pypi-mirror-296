import jpype 
from asposepdf import Assist 


class tagged_logicalstructure_elements_ils_RubyRTElement(Assist.BaseJavaClass):
    """!Represents RT structure element in logical structure of the Ruby."""

    java_class_name = "com.aspose.python.pdf.tagged.logicalstructure.elements.ils.RubyRTElement"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

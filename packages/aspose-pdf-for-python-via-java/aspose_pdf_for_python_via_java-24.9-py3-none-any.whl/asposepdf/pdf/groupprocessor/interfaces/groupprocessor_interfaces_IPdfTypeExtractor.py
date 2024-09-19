import jpype 
from asposepdf import Assist 


class groupprocessor_interfaces_IPdfTypeExtractor(Assist.BaseJavaClass):
    """!Represents interface to interacting with extractor."""

    java_class_name = "com.aspose.python.pdf.groupprocessor.interfaces.IPdfTypeExtractor"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

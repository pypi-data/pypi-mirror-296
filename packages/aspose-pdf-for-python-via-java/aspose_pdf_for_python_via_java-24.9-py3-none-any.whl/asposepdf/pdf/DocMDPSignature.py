import jpype 
from asposepdf import Assist 


class DocMDPSignature(Assist.BaseJavaClass):
    """!Represents the class of document MDP (modification detection and prevention) signature type."""

    java_class_name = "com.aspose.python.pdf.DocMDPSignature"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

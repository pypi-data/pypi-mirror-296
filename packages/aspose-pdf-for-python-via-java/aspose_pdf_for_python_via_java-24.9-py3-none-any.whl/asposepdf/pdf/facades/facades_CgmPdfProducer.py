import jpype 
from asposepdf import Assist 


class facades_CgmPdfProducer(Assist.BaseJavaClass):
    """!Represents a class to produce PDF from Computer Graphics Metafile(CGM) format."""

    java_class_name = "com.aspose.python.pdf.facades.CgmPdfProducer"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

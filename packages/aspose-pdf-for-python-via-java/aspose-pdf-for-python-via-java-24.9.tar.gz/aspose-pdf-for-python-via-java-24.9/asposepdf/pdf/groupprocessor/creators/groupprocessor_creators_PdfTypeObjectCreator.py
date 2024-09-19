import jpype 
from asposepdf import Assist 


class groupprocessor_creators_PdfTypeObjectCreator(Assist.BaseJavaClass):
    """!Represents an creator of IPdfTypeExtractor object."""

    java_class_name = "com.aspose.python.pdf.groupprocessor.creators.PdfTypeObjectCreator"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

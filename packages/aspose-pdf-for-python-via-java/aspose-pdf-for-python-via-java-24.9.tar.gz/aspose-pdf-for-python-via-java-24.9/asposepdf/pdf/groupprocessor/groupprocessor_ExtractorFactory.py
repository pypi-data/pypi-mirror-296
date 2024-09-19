import jpype 
from asposepdf import Assist 


class groupprocessor_ExtractorFactory(Assist.BaseJavaClass):
    """!Represents factory for creating IPdfTypeExtractor objects."""

    java_class_name = "com.aspose.python.pdf.groupprocessor.ExtractorFactory"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)


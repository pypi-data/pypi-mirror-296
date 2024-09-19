import jpype 
from asposepdf import Assist 


class vector_extraction_SubPathGroup(Assist.BaseJavaClass):
    """!Represents a class for a group of graphic element containers.
     Class objects have a bounding box to account for group size."""

    java_class_name = "com.aspose.python.pdf.vector.extraction.SubPathGroup"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

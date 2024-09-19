import jpype 
from asposepdf import Assist 


class PDF3DArtwork(Assist.BaseJavaClass):
    """!Class PDF3DArtwork."""

    java_class_name = "com.aspose.python.pdf.PDF3DArtwork"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

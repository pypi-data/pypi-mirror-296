import jpype 
from asposepdf import Assist 


class PDF3DStream(Assist.BaseJavaClass):
    """!Class PDF3DStream."""

    java_class_name = "com.aspose.python.pdf.PDF3DStream"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

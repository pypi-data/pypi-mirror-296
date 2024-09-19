import jpype 
from asposepdf import Assist 


class DestinationFactory(Assist.BaseJavaClass):
    """!Represents DestinationFactory class"""

    java_class_name = "com.aspose.python.pdf.DestinationFactory"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

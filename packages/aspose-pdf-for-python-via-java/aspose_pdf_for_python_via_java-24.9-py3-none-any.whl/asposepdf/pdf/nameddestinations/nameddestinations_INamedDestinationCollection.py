import jpype 
from asposepdf import Assist 


class nameddestinations_INamedDestinationCollection(Assist.BaseJavaClass):
    """!Collection of Named Destinations."""

    java_class_name = "com.aspose.python.pdf.nameddestinations.INamedDestinationCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

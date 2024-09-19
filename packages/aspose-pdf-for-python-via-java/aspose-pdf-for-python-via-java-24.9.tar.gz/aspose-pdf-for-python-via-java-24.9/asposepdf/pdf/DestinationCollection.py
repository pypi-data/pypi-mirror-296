import jpype 
from asposepdf import Assist 


class DestinationCollection(Assist.BaseJavaClass):
    """!Class represents the collection of all destinations (a name tree mapping name strings to
     destinations (see 12.3.2.3, "Named Destinations") and (see 7.7.4, "Name Dictionary")) in the pdf
     document."""

    java_class_name = "com.aspose.python.pdf.DestinationCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

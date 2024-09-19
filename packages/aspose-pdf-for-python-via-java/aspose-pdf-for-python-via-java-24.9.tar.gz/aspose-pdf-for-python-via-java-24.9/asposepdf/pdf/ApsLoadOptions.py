import jpype 
from asposepdf import Assist 


class ApsLoadOptions(Assist.BaseJavaClass):
    """!Class describes aps load options.
     Option for import from APS XML format."""

    java_class_name = "com.aspose.python.pdf.ApsLoadOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

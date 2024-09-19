import jpype 
from asposepdf import Assist 


class TextFragmentCollection(Assist.BaseJavaClass):
    """!Represents a text fragments collection"""

    java_class_name = "com.aspose.python.pdf.TextFragmentCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class TextSegmentCollection(Assist.BaseJavaClass):
    """!Represents a text segments collection"""

    java_class_name = "com.aspose.python.pdf.TextSegmentCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

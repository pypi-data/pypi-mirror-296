import jpype 
from asposepdf import Assist 


class OutlineItemCollection(Assist.BaseJavaClass):
    """!Represents outline entry in outline hierarchy of PDF document."""

    java_class_name = "com.aspose.python.pdf.OutlineItemCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

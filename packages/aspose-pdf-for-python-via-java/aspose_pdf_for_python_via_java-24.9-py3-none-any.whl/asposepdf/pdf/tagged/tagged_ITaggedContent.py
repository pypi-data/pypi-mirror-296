import jpype 
from asposepdf import Assist 


class tagged_ITaggedContent(Assist.BaseJavaClass):
    """!Represents interface for work with TaggedPdf content of document."""

    java_class_name = "com.aspose.python.pdf.tagged.ITaggedContent"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

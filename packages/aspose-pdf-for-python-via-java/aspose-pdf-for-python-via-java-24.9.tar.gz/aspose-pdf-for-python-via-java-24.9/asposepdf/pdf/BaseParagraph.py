import jpype 
from asposepdf import Assist 


class BaseParagraph(Assist.BaseJavaClass):
    """!Represents a abstract base object can be added to the page(doc.Paragraphs.Add())."""

    java_class_name = "com.aspose.python.pdf.BaseParagraph"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

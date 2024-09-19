import jpype 
from asposepdf import Assist 


class TextParagraphCollection(Assist.BaseJavaClass):
    """!Represents a text paragraphs collection"""

    java_class_name = "com.aspose.python.pdf.TextParagraphCollection"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

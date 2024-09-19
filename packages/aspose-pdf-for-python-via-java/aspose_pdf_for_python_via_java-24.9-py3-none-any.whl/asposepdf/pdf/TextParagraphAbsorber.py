import jpype 
from asposepdf import Assist 


class TextParagraphAbsorber(Assist.BaseJavaClass):
    """!Represents an absorber object of text paragraphs. Performs text search and provides access to
     search results via {@code TextParagraphAbsorber.TextParagraphs} collection."""

    java_class_name = "com.aspose.python.pdf.TextParagraphAbsorber"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

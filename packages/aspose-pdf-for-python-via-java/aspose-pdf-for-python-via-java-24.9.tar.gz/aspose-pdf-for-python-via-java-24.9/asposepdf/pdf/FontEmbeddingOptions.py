import jpype 
from asposepdf import Assist 


class FontEmbeddingOptions(Assist.BaseJavaClass):
    """!PDF/A standard requires, that all fonts must be embedded into document. This class includes flags
     for cases when it's not possible to embed some font cause this font is absent on destination PC."""

    java_class_name = "com.aspose.python.pdf.FontEmbeddingOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class text_SubstitutionFontCategories(Assist.BaseJavaClass):
    """!Represents font categories that can be substituted."""

    java_class_name = "com.aspose.python.pdf.text.SubstitutionFontCategories"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _AllEmbeddedFonts = 1
    _TheSameNamedEmbeddedFonts = 0

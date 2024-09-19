import jpype 
from asposepdf import Assist 


class FontAbsorber(Assist.BaseJavaClass):
    """!Represents an absorber object of fonts. Performs search for fonts and provides access to search
     results via {@code FontAbsorber.Fonts} collection."""

    java_class_name = "com.aspose.python.pdf.FontAbsorber"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

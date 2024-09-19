import jpype 
from asposepdf import Assist 


class vector_GraphicsAbsorber(Assist.BaseJavaClass):
    """!Represents an absorber object of graphics elements.
     Performs graphics search and provides access to search results via {@code GraphicsAbsorber.Elements}({@link GraphicsAbsorber#getElements}) collection."""

    java_class_name = "com.aspose.python.pdf.vector.GraphicsAbsorber"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

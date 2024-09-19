import jpype 
from asposepdf import Assist 


class markdownoptions_MarkdownSaveOptions(Assist.BaseJavaClass):
    """!Represents the document save option class in the markdown format."""

    java_class_name = "com.aspose.python.pdf.markdownoptions.MarkdownSaveOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

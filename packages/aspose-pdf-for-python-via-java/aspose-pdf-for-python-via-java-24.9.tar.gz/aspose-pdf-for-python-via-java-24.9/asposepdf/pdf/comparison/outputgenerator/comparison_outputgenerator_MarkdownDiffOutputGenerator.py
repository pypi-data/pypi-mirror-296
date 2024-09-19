import jpype 
from asposepdf import Assist 


class comparison_outputgenerator_MarkdownDiffOutputGenerator(Assist.BaseJavaClass):
    """!Represents a class for generating markdown representation of texts differences.
     Because of the markdown syntax, it is not possible to show changes to whitespace characters.
     Selection of changes makes adding whitespace characters around formatting,
     otherwise markdown viewer will not correctly display the text.
     Deleted line breaks are indicated by - paragraph mark."""

    java_class_name = "com.aspose.python.pdf.comparison.outputgenerator.MarkdownDiffOutputGenerator"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

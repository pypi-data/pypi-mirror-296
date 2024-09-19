import jpype 
from asposepdf import Assist 


class plugins_pdfgenerator_TocOptions(Assist.BaseJavaClass):
    """!Represents options for add table of contents to document by TocOptions plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.pdfgenerator.TocOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

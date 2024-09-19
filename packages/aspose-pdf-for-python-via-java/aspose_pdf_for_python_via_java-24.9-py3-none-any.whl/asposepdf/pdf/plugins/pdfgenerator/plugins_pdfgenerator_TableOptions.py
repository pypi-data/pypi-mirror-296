import jpype 
from asposepdf import Assist 


class plugins_pdfgenerator_TableOptions(Assist.BaseJavaClass):
    """!Represents options for add table to document by {@link TableGenerator} plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.pdfgenerator.TableOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class plugins_pdfgenerator_builder_TableRowBuilder(Assist.BaseJavaClass):
    """!Class represents builder for table row."""

    java_class_name = "com.aspose.python.pdf.plugins.pdfgenerator.builder.TableRowBuilder"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

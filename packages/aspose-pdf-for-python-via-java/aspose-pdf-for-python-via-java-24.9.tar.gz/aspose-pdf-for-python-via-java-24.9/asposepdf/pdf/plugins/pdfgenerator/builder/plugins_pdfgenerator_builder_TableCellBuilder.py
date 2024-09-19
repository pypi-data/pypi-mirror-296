import jpype 
from asposepdf import Assist 


class plugins_pdfgenerator_builder_TableCellBuilder(Assist.BaseJavaClass):
    """!Class represents builder for table cell."""

    java_class_name = "com.aspose.python.pdf.plugins.pdfgenerator.builder.TableCellBuilder"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

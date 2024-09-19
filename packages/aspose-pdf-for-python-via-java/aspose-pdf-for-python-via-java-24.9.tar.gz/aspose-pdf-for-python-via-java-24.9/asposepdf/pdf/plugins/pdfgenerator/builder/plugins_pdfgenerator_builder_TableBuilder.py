import jpype 
from asposepdf import Assist 


class plugins_pdfgenerator_builder_TableBuilder(Assist.BaseJavaClass):
    """!Class represents builder for table in pdf page."""

    java_class_name = "com.aspose.python.pdf.plugins.pdfgenerator.builder.TableBuilder"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

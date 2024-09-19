import jpype 
from asposepdf import Assist 


class plugins_formexporter_FormExporterOptions(Assist.BaseJavaClass):
    """!Represents options for FormExporter plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.formexporter.FormExporterOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

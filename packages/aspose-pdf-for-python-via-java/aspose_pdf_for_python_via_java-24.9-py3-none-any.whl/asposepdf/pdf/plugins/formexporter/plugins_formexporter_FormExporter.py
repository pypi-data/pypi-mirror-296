import jpype 
from asposepdf import Assist 


class plugins_formexporter_FormExporter(Assist.BaseJavaClass):
    """!Represents FormExporter plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.formexporter.FormExporter"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

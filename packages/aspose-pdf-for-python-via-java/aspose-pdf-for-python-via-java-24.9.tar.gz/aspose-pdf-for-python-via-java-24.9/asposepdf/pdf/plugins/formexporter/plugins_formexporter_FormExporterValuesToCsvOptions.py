import jpype 
from asposepdf import Assist 


class plugins_formexporter_FormExporterValuesToCsvOptions(Assist.BaseJavaClass):
    """!Represents options for export Value property(s) of specified field(s) (not annotations)."""

    java_class_name = "com.aspose.python.pdf.plugins.formexporter.FormExporterValuesToCsvOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

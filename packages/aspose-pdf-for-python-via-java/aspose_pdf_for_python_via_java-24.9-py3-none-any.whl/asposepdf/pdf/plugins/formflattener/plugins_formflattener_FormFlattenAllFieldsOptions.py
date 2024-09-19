import jpype 
from asposepdf import Assist 


class plugins_formflattener_FormFlattenAllFieldsOptions(Assist.BaseJavaClass):
    """!Represents options for flatten all fields (not annotations) in document by {@link FormFlattener} plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.formflattener.FormFlattenAllFieldsOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

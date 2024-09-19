import jpype 
from asposepdf import Assist 


class plugins_formflattener_FormFlattener(Assist.BaseJavaClass):
    """!Represents FormFlattener plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.formflattener.FormFlattener"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

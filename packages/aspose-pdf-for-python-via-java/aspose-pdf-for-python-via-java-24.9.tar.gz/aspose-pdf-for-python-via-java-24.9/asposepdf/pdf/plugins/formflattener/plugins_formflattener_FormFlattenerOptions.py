import jpype 
from asposepdf import Assist 


class plugins_formflattener_FormFlattenerOptions(Assist.BaseJavaClass):
    """!Base class for option classes for flatten fields (not annotations) in document by FormFlattener plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.formflattener.FormFlattenerOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

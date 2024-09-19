import jpype 
from asposepdf import Assist 


class Form_FlattenSettings(Assist.BaseJavaClass):
    """!Class which describes settings for Form flattening procedure."""

    java_class_name = "com.aspose.python.pdf.Form.FlattenSettings"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

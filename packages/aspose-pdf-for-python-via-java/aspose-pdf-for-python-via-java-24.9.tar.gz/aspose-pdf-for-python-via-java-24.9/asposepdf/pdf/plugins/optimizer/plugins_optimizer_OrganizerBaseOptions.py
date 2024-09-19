import jpype 
from asposepdf import Assist 


class plugins_optimizer_OrganizerBaseOptions(Assist.BaseJavaClass):
    """!Represents base options for plugins."""

    java_class_name = "com.aspose.python.pdf.plugins.optimizer.OrganizerBaseOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

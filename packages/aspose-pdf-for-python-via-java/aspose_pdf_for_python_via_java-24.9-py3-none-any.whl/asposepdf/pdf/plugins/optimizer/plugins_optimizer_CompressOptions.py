import jpype 
from asposepdf import Assist 


class plugins_optimizer_CompressOptions(Assist.BaseJavaClass):
    """!Represents Compress options for {@link Optimizer} plugin."""

    java_class_name = "com.aspose.python.pdf.plugins.optimizer.CompressOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

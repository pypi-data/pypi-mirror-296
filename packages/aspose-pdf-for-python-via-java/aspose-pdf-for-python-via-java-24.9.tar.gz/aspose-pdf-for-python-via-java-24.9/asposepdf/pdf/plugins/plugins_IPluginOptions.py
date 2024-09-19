import jpype 
from asposepdf import Assist 


class plugins_IPluginOptions(Assist.BaseJavaClass):
    """!General plugin option interface that defines common methods that concrete plugin option should implement."""

    java_class_name = "com.aspose.python.pdf.plugins.IPluginOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class plugins_IDataContainer(Assist.BaseJavaClass):
    """!General data container interface that defines common methods that concrete data container (plugin options) should implement."""

    java_class_name = "com.aspose.python.pdf.plugins.IDataContainer"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

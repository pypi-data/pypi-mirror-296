import jpype 
from asposepdf import Assist 


class plugins_IDataSource(Assist.BaseJavaClass):
    """!General data source interface that defines common members that concrete data sources should implement."""

    java_class_name = "com.aspose.python.pdf.plugins.IDataSource"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

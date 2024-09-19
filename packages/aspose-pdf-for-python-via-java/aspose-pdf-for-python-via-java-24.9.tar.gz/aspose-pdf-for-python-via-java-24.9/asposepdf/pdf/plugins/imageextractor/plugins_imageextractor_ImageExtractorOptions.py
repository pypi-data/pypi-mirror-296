import jpype 
from asposepdf import Assist 


class plugins_imageextractor_ImageExtractorOptions(Assist.BaseJavaClass):
    """!Represents images extraction options for the ImageExtractor plugin.
     
     It inherits functions to add data (files, streams) representing input PDF documents."""

    java_class_name = "com.aspose.python.pdf.plugins.imageextractor.ImageExtractorOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

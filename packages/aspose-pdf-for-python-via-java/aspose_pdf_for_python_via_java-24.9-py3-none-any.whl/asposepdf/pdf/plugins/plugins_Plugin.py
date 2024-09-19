import jpype 
from asposepdf import Assist 


class plugins_Plugin(Assist.BaseJavaClass):
    """!Represents possible plugins."""

    java_class_name = "com.aspose.python.pdf.plugins.Plugin"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _FormFlattener = 5
    _XlsConverter = 2
    _Splitter = 12
    _FormExporter = 4
    _Optimizer = 10
    _Png = 11
    _Html = 6
    _Jpeg = 8
    _TableGenerator = 13
    _TocGenerator = 15
    _Security = 19
    _FormEditor = 3
    _DocConverter = 16
    _Merger = 9
    _ChatGpt = 1
    _TextExtractor = 14
    _ImageExtractor = 7
    _None = 0

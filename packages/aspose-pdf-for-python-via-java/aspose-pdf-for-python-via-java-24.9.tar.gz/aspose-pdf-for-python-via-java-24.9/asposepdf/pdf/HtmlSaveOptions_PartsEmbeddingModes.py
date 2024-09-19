import jpype 
from asposepdf import Assist 


class HtmlSaveOptions_PartsEmbeddingModes(Assist.BaseJavaClass):
    """!This enum enumerates possible modes of embedding of files referenced in HTML It allows to
     control whether referenced files (HTML, Fonts,Images, CSSes) will be embedded into main HTML
     file or will be generated as apart binary entities"""

    java_class_name = "com.aspose.python.pdf.HtmlSaveOptions.PartsEmbeddingModes"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _NoEmbedding = 2
    _EmbedAllIntoHtml = 0
    _EmbedCssOnly = 1

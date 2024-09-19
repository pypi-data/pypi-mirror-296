import jpype 
from asposepdf import Assist 


class Document_IDocumentFontUtilities(Assist.BaseJavaClass):
    """!Holds functionality to tune fonts"""

    java_class_name = "com.aspose.python.pdf.Document.IDocumentFontUtilities"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class XmpPdfAExtensionProperty(Assist.BaseJavaClass):
    """!Describes a single property. Schema namespace URI: http://www.aiim.org/pdfa/ns/property# Required
     schema namespace prefix: pdfaProperty"""

    java_class_name = "com.aspose.python.pdf.XmpPdfAExtensionProperty"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

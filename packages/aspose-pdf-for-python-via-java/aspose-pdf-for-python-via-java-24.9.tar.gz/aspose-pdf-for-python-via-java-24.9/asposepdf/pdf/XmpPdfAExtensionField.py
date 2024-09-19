import jpype 
from asposepdf import Assist 


class XmpPdfAExtensionField(Assist.BaseJavaClass):
    """!This schema describes a field in a structured type. It is very similar to the PDF/A Property
     Value Type schema, but defines a field in a structure instead of a property. Schema namespace
     URI: http://www.aiim.org/pdfa/ns/field# Required schema namespace prefix: pdfaField."""

    java_class_name = "com.aspose.python.pdf.XmpPdfAExtensionField"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

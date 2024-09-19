import jpype 
from asposepdf import Assist 


class plugins_formeditor_FormFieldOptions(Assist.BaseJavaClass):
    """!Represents Field options. Base class for PdfFormFieldCreateOptions and PdfFormFillFieldOptions."""

    java_class_name = "com.aspose.python.pdf.plugins.formeditor.FormFieldOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

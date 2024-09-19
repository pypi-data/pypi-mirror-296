import jpype 
from asposepdf import Assist 


class BarcodeField(Assist.BaseJavaClass):
    """!Class represents barcode field."""

    java_class_name = "com.aspose.python.pdf.BarcodeField"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

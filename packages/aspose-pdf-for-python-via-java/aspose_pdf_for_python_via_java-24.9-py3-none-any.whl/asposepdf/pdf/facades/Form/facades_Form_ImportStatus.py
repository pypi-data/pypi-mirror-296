import jpype 
from asposepdf import Assist 


class facades_Form_ImportStatus(Assist.BaseJavaClass):
    """!Status of imported field"""

    java_class_name = "com.aspose.python.pdf.facades.Form.ImportStatus"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _FieldNotFound = 1
    _Success = 0

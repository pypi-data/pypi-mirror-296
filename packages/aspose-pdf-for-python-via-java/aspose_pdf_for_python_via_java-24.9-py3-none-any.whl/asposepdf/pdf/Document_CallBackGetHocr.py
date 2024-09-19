import jpype 
from asposepdf import Assist 


class Document_CallBackGetHocr(Assist.BaseJavaClass):
    """!The call back procedure for hocr recognize."""

    java_class_name = "com.aspose.python.pdf.Document.CallBackGetHocr"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

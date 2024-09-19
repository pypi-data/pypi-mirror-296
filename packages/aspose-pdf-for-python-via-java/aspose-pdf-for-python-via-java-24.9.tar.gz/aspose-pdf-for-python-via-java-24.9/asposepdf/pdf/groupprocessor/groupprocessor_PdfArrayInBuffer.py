import jpype 
from asposepdf import Assist 


class groupprocessor_PdfArrayInBuffer(Assist.BaseJavaClass):
    """!For internal usage only"""

    java_class_name = "com.aspose.python.pdf.groupprocessor.PdfArrayInBuffer"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

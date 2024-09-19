import jpype 
from asposepdf import Assist 


class HtmlSaveOptions_CssSavingStrategy(Assist.BaseJavaClass):
    """!You can assign to this property custom strategy that implements processing or/and saving of
     one CSS's part that was created during conversion of PDF to HTML . In such case processing
     (like saving to stream or disk) must be done in that custom code"""

    java_class_name = "com.aspose.python.pdf.HtmlSaveOptions.CssSavingStrategy"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

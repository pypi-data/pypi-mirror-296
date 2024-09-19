import jpype 
from asposepdf import Assist 


class Form_SignDependentElementsRenderingModes(Assist.BaseJavaClass):
    """!Forms can contain signing information and can be signed or unsigned. Sometimes view of forms
     in viewer must depend on whether form is signed or not. This enum enumerates possible
     rendering modes during conversion of form type in regard to sign."""

    java_class_name = "com.aspose.python.pdf.Form.SignDependentElementsRenderingModes"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _RenderFormAsUnsigned = 0
    _RenderFormAsSigned = 1

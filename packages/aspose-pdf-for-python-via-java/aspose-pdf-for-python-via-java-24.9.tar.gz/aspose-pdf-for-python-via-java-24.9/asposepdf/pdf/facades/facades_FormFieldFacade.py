import jpype 
from asposepdf import Assist 


class facades_FormFieldFacade(Assist.BaseJavaClass):
    """!Class for representing field properties."""

    java_class_name = "com.aspose.python.pdf.facades.FormFieldFacade"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _ALIGN_UNDEFINED = 3
    _BORDER_WIDTH_UNDEFINED = -1
    _ALIGN_CENTER = 1
    _BORDER_WIDTH_UNDIFIED = -1
    _BORDER_STYLE_INSET = 3
    _BORDER_STYLE_DASHED = 1
    _ALIGN_TOP = 0
    _BORDER_WIDTH_THICK = 3
    _BORDER_STYLE_UNDEFINED = 5
    _ALIGN_RIGHT = 2
    _ALIGN_BOTTOM = 2
    _ALIGN_LEFT = 0
    _BORDER_STYLE_BEVELED = 2
    _ALIGN_JUSTIFIED = 4
    _BORDER_WIDTH_MEDIUM = 2
    _BORDER_WIDTH_THIN = 1
    _ALIGN_MIDDLE = 1
    _BORDER_STYLE_SOLID = 0
    _BORDER_STYLE_UNDERLINE = 4

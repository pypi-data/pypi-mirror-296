import jpype 
from asposepdf import Assist 


class LoadOptions_PageSizeAdjustmentModes(Assist.BaseJavaClass):
    """!ATTENTION! The feature implemented but did not put yet to public API since blocker issue in
     OSHARED layer revealed for sample document.
     
     Represents mode of usage of page size during conversion. Formats (like HTML, EPUB etc),
     usually have float design, so, it allows to fit required pagesize. But sometimes content has
     specifies horizontal positions or size that does not allow put content into required page
     size. In such case we can define what should be done in this case (i.e when size of content
     does not fit required initial page size of result PDF document)."""

    java_class_name = "com.aspose.python.pdf.LoadOptions.PageSizeAdjustmentModes"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _EnlargeRequiredViewportWidthAndDoConversionAgain = 1
    _NoAjustmentAllwaysUsePredefinedSize = 0

import jpype 
from asposepdf import Assist 


class facades_IPdfFileEditor_ContentsResizeValue(Assist.BaseJavaClass):
    """!Value of margin or content size specified in percents of default space units.
     This class is used in ContentsResizeParameters."""

    java_class_name = "com.aspose.python.pdf.facades.IPdfFileEditor.ContentsResizeValue"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

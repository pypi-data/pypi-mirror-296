import jpype 
from asposepdf import Assist 


class facades_IPdfFileEditor_ContentsResizeParameters(Assist.BaseJavaClass):
    """!Class for specifing page resize parameters. Allow to set the following parameters: Size of
     result page (width, height) in default space units or in percents of initial pages size;
     Left, Top, Bottom and Right margins in default space units or in percents of initial page
     size; Some values may be left null for automatic calculation. These values will be calculated
     from rest of page size after calculation explicitly specified values. For example: if page
     width = 100 and new page width specified 60 units then left and right margins are
     automatically calculated: (100 - 60) / 2 = 15. This class is used in ResizeContents method."""

    java_class_name = "com.aspose.python.pdf.facades.IPdfFileEditor.ContentsResizeParameters"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

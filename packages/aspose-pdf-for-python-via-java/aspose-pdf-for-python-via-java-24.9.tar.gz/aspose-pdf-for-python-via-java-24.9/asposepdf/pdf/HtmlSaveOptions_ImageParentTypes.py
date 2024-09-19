import jpype 
from asposepdf import Assist 


class HtmlSaveOptions_ImageParentTypes(Assist.BaseJavaClass):
    """!Enumerates possible types of image's parents Image can pertain to HTML page or to SVG parent
     image"""

    java_class_name = "com.aspose.python.pdf.HtmlSaveOptions.ImageParentTypes"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

    _HtmlPage = 0
    _SvgImage = 1

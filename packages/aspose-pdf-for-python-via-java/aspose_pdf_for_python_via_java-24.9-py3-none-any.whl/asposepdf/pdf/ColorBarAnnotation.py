import jpype 
from asposepdf import Assist 


class ColorBarAnnotation(Assist.BaseJavaClass):
    """!Class representing ColorBarAnnotation annotation.
     Property Color ignored, instead used ColorsOfCMYK color.
     On creation, the ratio of width and height determines the orientation of the annotation - horizontal or vertical.
     Next, it checks that the annotation rectangle is outside the TrimBox, and if not, then it is shifted to the nearest location outside the TrimBox,
     taking into account the orientation of the annotation. It is possible to reduce the width (height) so that the annotation fits outside the TrimBox.
     If there is no space for the layout, the width/height can be set to zero (in this case, the annotation is present on the page, but not displayed)."""

    java_class_name = "com.aspose.python.pdf.ColorBarAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

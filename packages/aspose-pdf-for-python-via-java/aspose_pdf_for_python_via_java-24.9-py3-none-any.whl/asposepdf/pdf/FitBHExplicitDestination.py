import jpype 
from asposepdf import Assist 


class FitBHExplicitDestination(Assist.BaseJavaClass):
    """!Represents explicit destination that displays the page with the vertical coordinate top
     positioned at the top edge of the window and the contents of the page magnified just enough to
     fit the entire width of its bounding box within the window. A null value for top specifies that
     the current value of that parameter is to be retained unchanged."""

    java_class_name = "com.aspose.python.pdf.FitBHExplicitDestination"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

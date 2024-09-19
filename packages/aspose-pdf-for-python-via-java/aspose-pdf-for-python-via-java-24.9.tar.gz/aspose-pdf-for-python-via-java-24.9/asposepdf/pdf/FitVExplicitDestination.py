import jpype 
from asposepdf import Assist 


class FitVExplicitDestination(Assist.BaseJavaClass):
    """!Represents explicit destination that displays the page with the horizontal coordinate left
     positioned at the left edge of the window and the contents of the page magnified just enough to
     fit the entire height of the page within the window. A null value for left specifies that the
     current value of that parameter is to be retained unchanged."""

    java_class_name = "com.aspose.python.pdf.FitVExplicitDestination"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class FitExplicitDestination(Assist.BaseJavaClass):
    """!Represents explicit destination that displays the page with its contents magnified just enough to
     fit the entire page within the window both horizontally and vertically. If the required
     horizontal and vertical magnification factors are different, use the smaller of the two,
     centering the page within the window in the other dimension."""

    java_class_name = "com.aspose.python.pdf.FitExplicitDestination"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

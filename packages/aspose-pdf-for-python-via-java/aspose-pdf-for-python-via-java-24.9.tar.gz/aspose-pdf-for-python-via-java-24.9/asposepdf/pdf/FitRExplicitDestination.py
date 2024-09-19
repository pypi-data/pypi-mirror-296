import jpype 
from asposepdf import Assist 


class FitRExplicitDestination(Assist.BaseJavaClass):
    """!Represents explicit destination that displays the page with its contents magnified just enough to
     fit the rectangle specified by the coordinates left, bottom, right, and topentirely within the
     window both horizontally and vertically. If the required horizontal and vertical magnification
     factors are different, use the smaller of the two, centering the rectangle within the window in
     the other dimension. A null value for any of the parameters may result in unpredictable behavior."""

    java_class_name = "com.aspose.python.pdf.FitRExplicitDestination"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

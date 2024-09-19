import jpype 
from asposepdf import Assist 


class ExplicitDestinationType(Assist.BaseJavaClass):
    """!Enumerates the types of explicit destinations."""

    java_class_name = "com.aspose.python.pdf.ExplicitDestinationType"
    java_class = jpype.JClass(java_class_name)

    XYZ = java_class.XYZ
    """!
     Display the page with the coordinates (left, top) positioned at the upper-left corner of the
     window and the contents of the page magnified by the factor zoom. A null value for any of the
     parameters left, top, or zoom specifies that the current value of that parameter is to be
     retained unchanged. A zoom value of 0 has the same meaning as a null value.
    
    """

    Fit = java_class.Fit
    """!
     Display the page with its contents magnified just enough to fit the entire page within the
     window both horizontally and vertically. If the required horizontal and vertical
     magnification factors are different, use the smaller of the two, centering the page within
     the window in the other dimension.
    
    """

    FitH = java_class.FitH
    """!
     Display the page with the vertical coordinate top positioned at the top edge of the window
     and the contents of the page magnified just enough to fit the entire width of the page within
     the window. A null value for top specifies that the current value of that parameter is to be
     retained unchanged.
    
    """

    FitV = java_class.FitV
    """!
     Display the page with the horizontal coordinate left positioned at the left edge of the
     window and the contents of the page magnified just enough to fit the entire height of the
     page within the window. A null value for left specifies that the current value of that
     parameter is to be retained unchanged.
    
    """

    FitR = java_class.FitR
    """!
     Display the page with its contents magnified just enough to fit the rectangle specified by
     the coordinates left, bottom, right, and topentirely within the window both horizontally and
     vertically. If the required horizontal and vertical magnification factors are different, use
     the smaller of the two, centering the rectangle within the window in the other dimension. A
     null value for any of the parameters may result in unpredictable behavior.
    
    """

    FitB = java_class.FitB
    """!
     Display the page with its contents magnified just enough to fit its bounding box entirely
     within the window both horizontally and vertically. If the required horizontal and vertical
     magnification factors are different, use the smaller of the two, centering the bounding box
     within the window in the other dimension.
    
    """

    FitBH = java_class.FitBH
    """!
     Display the page with the vertical coordinate top positioned at the top edge of the window
     and the contents of the page magnified just enough to fit the entire width of its bounding
     box within the window. A null value for top specifies that the current value of that
     parameter is to be retained unchanged.
    
    """

    FitBV = java_class.FitBV
    """!
     Display the page with the horizontal coordinate left positioned at the left edge of the
     window and the contents of the page magnified just enough to fit the entire height of its
     bounding box within the window. A null value for left specifies that the current value of
     that parameter is to be retained unchanged.
    
    """


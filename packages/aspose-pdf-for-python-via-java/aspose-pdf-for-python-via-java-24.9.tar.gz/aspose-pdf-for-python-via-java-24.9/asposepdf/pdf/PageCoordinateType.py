import jpype 
from asposepdf import Assist 


class PageCoordinateType(Assist.BaseJavaClass):
    """!Describes page coordinate type.
     MediaBox = 0 </br>
     CropBox = 1"""

    java_class_name = "com.aspose.python.pdf.PageCoordinateType"
    java_class = jpype.JClass(java_class_name)

    MediaBox = java_class.MediaBox
    """!
     The MediaBox is used to specify the width and height of the page. For the average user, this
     probably equals the actual page size. The MediaBox is the largest page box in a PDF. The
     other page boxes can equal the size of the MediaBox but they cannot be larger.
    
    """

    CropBox = java_class.CropBox
    """!
     The CropBox defines the region to which the page contents are to be clipped. Acrobat uses
     this size for screen display and printing.
    
    """


import jpype 
from asposepdf import Assist 


class PageLayout(Assist.BaseJavaClass):
    """!Descibes page layout."""

    java_class_name = "com.aspose.python.pdf.PageLayout"
    java_class = jpype.JClass(java_class_name)

    SinglePage = java_class.SinglePage
    """!
     Single page.
    
    """

    OneColumn = java_class.OneColumn
    """!
     Display the pages in one column.
    
    """

    TwoColumnLeft = java_class.TwoColumnLeft
    """!
     Display the pages in two columns, with odd-numbered pages on the left.
    
    """

    TwoColumnRight = java_class.TwoColumnRight
    """!
     Display the pages in two columns, with odd-numbered pages on the right.
    
    """

    TwoPageLeft = java_class.TwoPageLeft
    """!
     Display the pages two at a time, with odd-numbered pages on the left.
    
    """

    TwoPageRight = java_class.TwoPageRight
    """!
     Display the pages two at a time, with odd-numbered pages on the right.
    
    """

    Default = java_class.Default
    """!
     Default layout.
    
    """


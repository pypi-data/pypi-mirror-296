import jpype 
from asposepdf import Assist 


class LoadFormat(Assist.BaseJavaClass):
    """!Specifies load format."""

    java_class_name = "com.aspose.python.pdf.LoadFormat"
    java_class = jpype.JClass(java_class_name)

    CGM = java_class.CGM
    """!
     means loading of document in CGM format
    
    """

    HTML = java_class.HTML
    """!
     means loading of document in HTML format
    
    """

    EPUB = java_class.EPUB
    """!
     means loading of document in EPUB format(special format of e-books)
    
    """

    XML = java_class.XML
    """!
     means loading of document in XML format(special XML that represent logical structure of PDF
     document)
    
    """

    XSLFO = java_class.XSLFO
    """!
     means loading of document in XSLFO format
    
    """

    PCL = java_class.PCL
    """!
     means loading of document in PCL format
    
    """

    XPS = java_class.XPS
    """!
     means loading of document in XPS format
    
    """

    TEX = java_class.TEX
    """!
     means loading of document in TEX format - format of Latex text editor
    
    """

    SVG = java_class.SVG
    """!
     means loading of document in SVG format - format of Latex text editor
    
    """

    MHT = java_class.MHT
    """!
     means loading of document in MHT format(that is packed HTML format)
    
    """

    PS = java_class.PS
    """!
     means loading of document in PS format(format of PostScript document)
    
    """

    MD = java_class.MD
    """!
     means loading document is in MD format (markdown).
    
    """

    TXT = java_class.TXT
    """!
     means loading document is in TXT format.
    
    """

    APS = java_class.APS
    """!
     means loading document in APS format.
    
    """

    PDFXML = java_class.PDFXML
    """!
     Internal PDF document structure in XML format.
    
    """

    OFD = java_class.OFD
    """!
     means loading document in OFD format.
    
    """

    DJVU = java_class.DJVU
    """!
     means loading document in Djvu format.
    
    """

    CDR = java_class.CDR
    """!
     means loading document in CDR format.
    
    """


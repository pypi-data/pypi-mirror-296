import jpype 
from asposepdf import Assist 


class SaveFormat(Assist.BaseJavaClass):
    """!Specifies format"""

    java_class_name = "com.aspose.python.pdf.SaveFormat"
    java_class = jpype.JClass(java_class_name)

    Pdf = java_class.Pdf
    """!
     means saving without change of format, i.e. as PDF use it please instead of
     'SaveFormat.None', that is obsolete one
    
    """

    Nothing = 0 #get element java_class.getByValue(0) None is reserved word in python - replaced to Nothing
    """!
    """

    Doc = java_class.Doc
    """!
     means saving in DOC format
    
    """

    Xps = java_class.Xps
    """!
     means saving in XPS format
    
    """

    Html = java_class.Html
    """!
     means saving in HTML format
    
    """

    Xml = java_class.Xml
    """!
     means saving in XML format
    
    """

    TeX = java_class.TeX
    """!
     means saving in TEX format i.e. format suitable for Latex text editor
    
    """

    DocX = java_class.DocX
    """!
     means saving in DOCX format
    
    """

    Svg = java_class.Svg
    """!
     means saving in SVG format
    
    """

    MobiXml = java_class.MobiXml
    """!
     means saving in MobiXML format(special format of e-books)
    
    """

    Excel = java_class.Excel
    """!
     means saving in MsExcel format
    
    """

    Epub = java_class.Epub
    """!
     means saving in EPUB format(special format of e-books)
    
    """

    Pptx = java_class.Pptx
    """!
     means saving in MHT(WebArchieve) ///
     
     Convet document to Mht format. This code was experimental one used during works related to
     https://pdf.aspose.com/jira/browse/PDFNEWNET-36340 is not going on production, cause there
     are cross-browsers problems with created MHT - so, it can be used in the future if finally it
     will be necessary to create MHT itself. PDFNEWNET-36340 was resolved with usage of DataSceme
     URLs(embedding data into HTML http://en.wikipedia.org/wiki/Data_URI_scheme) So, this
     conversion really not used right now.
     
     means saving in PPTX format
    
    """

    Aps = java_class.Aps
    """!
     Saving as APS XML file.
    
    """

    PdfXml = java_class.PdfXml
    """!
     Internal PDF document structure in XML format
    
    """

    Ps = java_class.Ps
    """!
     means saving in PostScript format.
    
    """

    Eps = java_class.Eps
    """!
     means saving in Encapsulated PostScript format.
    
    """

    Markdown = java_class.Markdown
    """!
     means saving in Markdown format.
    
    """


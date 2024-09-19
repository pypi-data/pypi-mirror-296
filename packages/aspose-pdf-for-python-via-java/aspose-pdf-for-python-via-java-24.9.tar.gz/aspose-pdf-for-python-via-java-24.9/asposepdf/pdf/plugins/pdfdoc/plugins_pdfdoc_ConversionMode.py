import jpype 
from asposepdf import Assist 


class plugins_pdfdoc_ConversionMode(Assist.BaseJavaClass):
    """!Defines conversion mode of the output document."""

    java_class_name = "com.aspose.python.pdf.plugins.pdfdoc.ConversionMode"
    java_class = jpype.JClass(java_class_name)

    TextBox = java_class.TextBox
    """!
     This mode is fast and good for maximally preserving original look of the PDF file,
     but editability of the resulting document could be limited.
     Every visually grouped block of text int the original PDF file is converted into a textbox
     in the resulting document. This achieves maximal resemblance of the output document to the original
     PDF file. The output document will look good, but it will consist entirely of textboxes and it
     could makes further editing of the document in Microsoft Word quite hard.
     This is the default mode.
    
    """

    Flow = java_class.Flow
    """!
     Full recognition mode, the engine performs grouping and multi-level analysis to restore
     the original document author's intent and produce a maximally editable document.
     The downside is that the output document might look different from the original PDF file.
    
    """

    EnhancedFlow = java_class.EnhancedFlow
    """!
     An alternative Flow mode that supports the recognition of tables.
    
    """


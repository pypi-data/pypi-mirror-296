import jpype 
from asposepdf import Assist 


class DocSaveOptions_DocFormat(Assist.BaseJavaClass):
    """!Allows to specify .doc or .docx file format."""

    java_class_name = "com.aspose.python.pdf.DocSaveOptions.DocFormat"
    java_class = jpype.JClass(java_class_name)

    Doc = java_class.Doc
    """!
     [MS-DOC]: Word (.doc) Binary File Format
    
    """

    DocX = java_class.DocX
    """!
     Office Open XML (.docx) File Format
    
    """


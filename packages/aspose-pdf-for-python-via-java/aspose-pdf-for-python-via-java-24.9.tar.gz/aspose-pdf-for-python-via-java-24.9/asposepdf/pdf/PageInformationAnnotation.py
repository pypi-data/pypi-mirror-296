import jpype 
from asposepdf import Assist 


class PageInformationAnnotation(Assist.BaseJavaClass):
    """!Represents a Page Information annotation in a PDF document. This annotation contains the file name,
     page number, and the date and time of the annotation creation.
     
     This class is primarily used to add metadata to a specific page in the PDF document, which can be useful
     for tracking and referencing purposes. For instance, it can be used to mark pages during the printing process
     or to provide additional information about the page when viewing the document."""

    java_class_name = "com.aspose.python.pdf.PageInformationAnnotation"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

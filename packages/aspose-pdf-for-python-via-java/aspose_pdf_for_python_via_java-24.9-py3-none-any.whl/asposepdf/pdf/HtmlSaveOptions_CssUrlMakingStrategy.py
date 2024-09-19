import jpype 
from asposepdf import Assist 


class HtmlSaveOptions_CssUrlMakingStrategy(Assist.BaseJavaClass):
    """!You can assign to this property delegate created from custom method that implements creation
     of URL of CSS referenced in generated HTML document. F.e. if You want to make CSS referenced
     in HTML f.e. as "otherPage.ASPX?CssID=zjjkklj" Then such custom strategy must return
     "otherPage.ASPX?CssID=zjjkklj""""

    java_class_name = "com.aspose.python.pdf.HtmlSaveOptions.CssUrlMakingStrategy"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

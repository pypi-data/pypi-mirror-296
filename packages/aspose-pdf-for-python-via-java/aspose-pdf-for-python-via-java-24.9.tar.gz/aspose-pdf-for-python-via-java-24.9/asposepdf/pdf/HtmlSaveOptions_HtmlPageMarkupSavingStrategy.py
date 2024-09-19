import jpype 
from asposepdf import Assist 


class HtmlSaveOptions_HtmlPageMarkupSavingStrategy(Assist.BaseJavaClass):
    """!Result of conversion can contain one or several HTML-pages ( that also can reference external
     files like images or fonts) You can assign to this property delegate created from custom
     method that implements processing of got HTML-page(HTML itself) that was created during
     conversion. In such case processing (like saving in stream or disk) can be done in that
     custom code . In such case All the necessary actions for saving of HTML page's markup must be
     undertaken in code of supplied method, because saving of result in code of converter will be
     not in use. If processing for this or that case for some reason must be done by converter's
     code itself, not in custom code, please set in custom code flag 'CustomProcessingCancelled'
     of 'htmlSavingInfo' parameter's variable : it signals to converter that all the necessary
     steps for processing of that resource must be done in converter itself in same way as if
     there was no any external custom saving code ."""

    java_class_name = "com.aspose.python.pdf.HtmlSaveOptions.HtmlPageMarkupSavingStrategy"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

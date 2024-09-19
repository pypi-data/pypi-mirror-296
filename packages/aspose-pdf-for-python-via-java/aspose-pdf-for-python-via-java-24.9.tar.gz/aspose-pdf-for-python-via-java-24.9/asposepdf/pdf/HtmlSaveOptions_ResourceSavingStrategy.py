import jpype 
from asposepdf import Assist 


class HtmlSaveOptions_ResourceSavingStrategy(Assist.BaseJavaClass):
    """!To this property You can assign delegate created from custom method that implements
     processing of external resource(Font or Image) that was extracted from PDF and must be saved
     as external resource during conversion of PDF to HTML. In such case processing (like saving
     in stream or disk) can be done in that custom code and that custom code must return path(or
     any another string without quotemarks) that will be afterwards incorporated into generated
     HTML instead of original supposed path to that image resource. In such case All the necessary
     actions for saving of image must be undertaken in code of supplied method, because saving of
     result in code of converter will be not in use . If processing for this or that file for some
     reason must be done by converter's code itself, not in custom code, please set in custom code
     flag 'CustomProcessingCancelled' of 'resourceSavingInfo' parameter's variable It signals to
     converter that all the necessary steps for processing of that resource must be done in
     converter itself as if there was no any external custom code ."""

    java_class_name = "com.aspose.python.pdf.HtmlSaveOptions.ResourceSavingStrategy"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

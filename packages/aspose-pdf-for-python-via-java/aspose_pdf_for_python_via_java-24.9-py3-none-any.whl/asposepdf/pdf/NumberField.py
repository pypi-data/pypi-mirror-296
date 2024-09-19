import jpype 
from asposepdf import Assist 


class NumberField(Assist.BaseJavaClass):
    """!Text Field with specified valid chars
     
     @see TextBoxField"""

    java_class_name = "com.aspose.python.pdf.NumberField"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

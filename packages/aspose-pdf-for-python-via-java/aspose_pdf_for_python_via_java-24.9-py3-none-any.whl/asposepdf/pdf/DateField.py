import jpype 
from asposepdf import Assist 


class DateField(Assist.BaseJavaClass):
    """!Date field with calendar view.
     
     DateField dateField = new DateField(page, rect);
     doc.getForm().add(dateField);
     dateField.init(page);
     
     @see TextBoxField"""

    java_class_name = "com.aspose.python.pdf.DateField"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

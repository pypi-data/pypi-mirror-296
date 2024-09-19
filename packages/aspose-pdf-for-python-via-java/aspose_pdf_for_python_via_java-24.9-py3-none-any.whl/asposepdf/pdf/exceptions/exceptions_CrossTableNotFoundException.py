import jpype 
from asposepdf import Assist 


class exceptions_CrossTableNotFoundException(Assist.BaseJavaClass):
    """!Represents CrossTableNotFoundException class"""

    java_class_name = "com.aspose.python.pdf.exceptions.CrossTableNotFoundException"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

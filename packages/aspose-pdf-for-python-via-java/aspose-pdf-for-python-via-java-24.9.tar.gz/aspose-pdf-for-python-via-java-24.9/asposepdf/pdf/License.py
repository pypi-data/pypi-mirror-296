import jpype 
from asposepdf import Assist 


class License(Assist.BaseJavaClass):
    """!Provides methods to license the component.
     In this example, an attempt will be made to find a license file named MyLicense.lic in the folder
     that contains the component, in the folder that contains the calling assembly, in the folder of
     the entry assembly and then in the embedded resources of the calling assembly.
     
     License license = new License();</br>
     license.setLicense("MyLicense.lic");"""

    java_class_name = "com.aspose.python.pdf.License"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class plugins_security_Security(Assist.BaseJavaClass):
    """!Represents {@link Security} plugin.
     
     The example demonstrates how to encrypt PDF document.
     // create Security
     Security plugin = new Security();
     // create EncryptionOptions object to set instructions
     var opt = new EncryptionOptions("123456", "qwerty", DocumentPrivilege.ForbidAll));
     // add input file path
     opt.addInput(new FileDataSource(inputPath));
     // set output file path
     opt.addOutput(new FileDataSource(outputPath));
     // perform the process
     plugin.process(opt);
     
     The example demonstrates how to decrypt PDF document.
     // create Security
     Security plugin = new Security();
     // create DecryptionOptions object to set instructions
     DecryptionOptions opt = new DecryptionOptions("123456"));
     // add input file path
     opt.addInput(new FileDataSource(inputPath));
     // set output file path
     opt.addOutput(new FileDataSource(outputPath));
     // perform the process
     plugin.process(opt);"""

    java_class_name = "com.aspose.python.pdf.plugins.security.Security"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

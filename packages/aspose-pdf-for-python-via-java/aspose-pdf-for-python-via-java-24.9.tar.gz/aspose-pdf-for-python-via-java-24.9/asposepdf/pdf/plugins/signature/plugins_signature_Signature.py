import jpype 
from asposepdf import Assist 


class plugins_signature_Signature(Assist.BaseJavaClass):
    """!Represents {@link Signature} plugin.
     The example demonstrates how to sign PDF document.
     // create Signature
     Signature plugin = new Signature();
     // create SignOptions object to set instructions
     AddSignauteOptions opt = new SignOptions(inputPfx, inputPfxPassword);
     // add input file paths
     opt.addInput(new FileDataSource(inputPath));
     // set output file path
     opt.addOutput(new FileDataSource(outputPath));
     // perform the process
     plugin.process(opt);"""

    java_class_name = "com.aspose.python.pdf.plugins.signature.Signature"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

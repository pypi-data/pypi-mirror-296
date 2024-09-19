import jpype 
from asposepdf import Assist 


class plugins_pdfgenerator_TableGenerator(Assist.BaseJavaClass):
    """!Represents TableGenerator plugin.
     The example demonstrates how to add table to PDF file.
     
     // create TableGenerator
     TableGenerator generator = new TableGenerator();
     // create TableOptions object to set instructions
     TableOptions opt = new TableOptions();
     // add input file paths
     opt.addInput(new FileDataSource(inputPath1));
     opt.addInput(new FileDataSource(inputPath2));
     // set output file path
     opt.addOutput(new FileDataSource(outputPath));
     // perform extraction process
     generator.process(opt);"""

    java_class_name = "com.aspose.python.pdf.plugins.pdfgenerator.TableGenerator"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

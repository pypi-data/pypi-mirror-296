import jpype 
from asposepdf import Assist 


class plugins_pdfgenerator_TocGenerator(Assist.BaseJavaClass):
    """!Represents Aspose.PDF TocGenerator plugin.
     The example demonstrates how to add TOC to PDF file.
     // create TocGenerator
     TocGenerator generator = new TocGenerator();
     // create TocOptions object to set instructions
     TocOptions opt = new TocOptions();
     // add input file paths
     opt.addInput(new FileDataSource(inputPath1));
     opt.addInput(new FileDataSource(inputPath2));
     // set output file path
     opt.addOutput(new FileDataSource(outputPath));
     // perform extraction process
     generator.process(opt);"""

    java_class_name = "com.aspose.python.pdf.plugins.pdfgenerator.TocGenerator"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

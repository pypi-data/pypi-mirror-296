import jpype 
from asposepdf import Assist 


class plugins_splitter_Splitter(Assist.BaseJavaClass):
    """!Represents {@link Splitter} plugin.
     The example demonstrates how to split PDF document.
     // create Splitter
     Splitter splitter = new Splitter();
     // create SplitOptions object to set instructions
     SplitOptions opt = new SplitOptions();
     // add input file paths
     opt.addInput(new FileDataSource(inputPath));
     // set output file paths
     opt.addOutput(new FileDataSource(outputPath1));
     opt.addOutput(new FileDataSource(outputPath2));
     // perform the process
     splitter.process(opt);"""

    java_class_name = "com.aspose.python.pdf.plugins.splitter.Splitter"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

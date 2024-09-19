import jpype 
from asposepdf import Assist 


class plugins_merger_Merger(Assist.BaseJavaClass):
    """!Represents {@link Merger} plugin.
     The example demonstrates how to merge two PDF documents.
     // create Merger
     Merger merger = new Merger();
     // create MergeOptions object to set instructions
     MergeOptions opt = new MergeOptions();
     // add input file paths
     opt.addInput(new FileDataSource(inputPath1));
     opt.addInput(new FileDataSource(inputPath2));
     // set output file path
     opt.addOutput(new FileDataSource(outputPath));
     // perform the process
     merger.process(opt);"""

    java_class_name = "com.aspose.python.pdf.plugins.merger.Merger"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

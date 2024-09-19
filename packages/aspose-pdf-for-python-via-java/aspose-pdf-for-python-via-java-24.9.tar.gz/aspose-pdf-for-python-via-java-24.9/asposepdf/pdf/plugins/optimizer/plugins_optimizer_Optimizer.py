import jpype 
from asposepdf import Assist 


class plugins_optimizer_Optimizer(Assist.BaseJavaClass):
    """!Represents {@link Optimizer} plugin.
     
     The example demonstrates how to optimize PDF document.
     // create Optimizer
     Optimizer optimizer = new Optimizer();
     // create OptimizeOptions object to set instructions
     OptimizeOptions opt = new OptimizeOptions();
     // add input file paths
     opt.addInput(new FileDataSource(inputPath));
     // set output file path
     opt.addOutput(new FileDataSource(outputPath));
     // perform the process
     optimizer.process(opt);"""

    java_class_name = "com.aspose.python.pdf.plugins.optimizer.Optimizer"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

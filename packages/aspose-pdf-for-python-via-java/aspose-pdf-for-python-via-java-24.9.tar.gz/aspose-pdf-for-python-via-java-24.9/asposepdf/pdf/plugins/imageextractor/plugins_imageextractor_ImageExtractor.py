import jpype 
from asposepdf import Assist 


class plugins_imageextractor_ImageExtractor(Assist.BaseJavaClass):
    """!Represents ImageExtractor plugin.
     The example demonstrates how to extract images from PDF document.
     
     // create ImageExtractor object to extract images
     ImageExtractor extractor = new ImageExtractor();
     // create ImageExtractorOptions
     imageExtractorOptions = new ImageExtractorOptions();
     // add input file path to data sources
     imageExtractor.addDataSource(new FileDataSource(inputPath));
     // perform extraction process
     ResultContainer resultContainer = extractor.process(imageExtractorOptions);
     // get the image from the ResultContainer object
     String imageExtracted = resultContainer.getResultCollection().get_Item(0).toFile();
     extractor.close();
     
     The {@link ImageExtractor} object is used to extract text in PDF documents."""

    java_class_name = "com.aspose.python.pdf.plugins.imageextractor.ImageExtractor"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

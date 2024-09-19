import jpype 
from asposepdf import Assist 


class plugins_textextractor_TextExtractor(Assist.BaseJavaClass):
    """!Represents TextExtractor plugin.
     
     The example demonstrates how to extract text content of PDF document.
     // create TextExtractor object to extract text in PDF contents
     TextExtractor extractor = new TextExtractor();
     {
     // create TextExtractorOptions
     TextExtractorOptions textExtractorOptions = new TextExtractorOptions();
     // add input file path to data sources
     textExtractorOptions.addDataSource(new FileDataSource(inputPath));
     // perform extraction process
     ResultContainer resultContainer = extractor.process(textExtractorOptions);
     // get the extracted text from the ResultContainer object
     string textExtracted = resultContainer.getResultCollection().get().toString();
     }
     The {@link TextExtractor} object is used to extract text in PDF documents."""

    java_class_name = "com.aspose.python.pdf.plugins.textextractor.TextExtractor"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

import jpype 
from asposepdf import Assist 


class plugins_textextractor_TextExtractorOptions(Assist.BaseJavaClass):
    """!Represents text extraction options for the TextExtractor plugin.
     
     The example demonstrates how to extract text content of PDF document.
     // create TextExtractor object to extract PDF contents
     TextExtractor extractor = new TextExtractor();
     {
     // create TextExtractorOptions object to set TextFormattingMode (Pure,  or Raw - default)
     TextExtractorOptions extractorOptions = new TextExtractorOptions(TextExtractorOptions.TextFormattingMode.Pure);
     // add input file path to data sources
     extractorOptions.addInput(new FileDataSource(inputPath));
     // perform extraction process
     ResultContainer resultContainer = extractor.process(extractorOptions);
     // get the extracted text from the ResultContainer object
     string textExtracted = resultContainer.getResultCollection().get().toString();
     }
     
     The {@link TextExtractorOptions} object is used to set {@link TextExtractorOptions.TextFormattingMode} and another options for the text extraction operation.
     Also, it inherits functions to add data (files, streams) representing input PDF documents."""

    java_class_name = "com.aspose.python.pdf.plugins.textextractor.TextExtractorOptions"
    java_class = jpype.JClass(java_class_name)

    def __init__(self):
        java_object = self.java_class()
        super().__init__(java_object)

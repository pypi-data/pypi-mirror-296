
from asposepdf import Assist


class BaseParagraph(Assist.BaseJavaClass):
    """!
    Represents an abstract base object can be added to the page.
    """

    javaClassName = "com.aspose.python.pdf.BaseParagraph"

    def getVerticalAlignment(self):
        """!
        Gets a vertical alignment of paragraph
        """
        return self.get_java_object().getVerticalAlignment()

    def setVerticalAlignment(self, verticalAlignment):
        """!
        Sets a vertical alignment of paragraph
        """
        self.get_java_object().setVerticalAlignment(verticalAlignment)

    def getHorizontalAlignment(self):
        """!
        Gets a horizontal alignment of paragraph
        """
        return self.get_java_object().getHorizontalAlignment()

    def setHorizontalAlignment(self, horizontalAlignment):
        """!
        Sets a horizontal alignment of paragraph
        """
        self.get_java_object().setHorizontalAlignment(horizontalAlignment)

    def isFirstParagraphInColumn(self):
        """!
        Gets a bool value that indicates whether this paragraph will be at next column.
        Default is false.(for pdf generation)
        """
        return self.get_java_object().isFirstParagraphInColumn()

    def setFirstParagraphInColumn(self, value):
        """!
        Sets a bool value that indicates whether this paragraph will be at next column.
        Default is false.(for pdf generation)
        """
        self.get_java_object().setFirstParagraphInColumn(value)

    def isKeptWithNext(self):
        """!
        Gets a boolean value that indicates whether current paragraph remains in the same page along
        with next paragraph. Default is false.(for pdf generation)
        """
        return self.get_java_object().isKeptWithNext()

    def setKeptWithNext(self, value):
        """!
        Sets a boolean value that indicates whether current paragraph remains in the same page along
        with next paragraph. Default is false.(for pdf generation)
        """
        self.get_java_object().setKeptWithNext(value)

    def isInNewPage(self):
        """!
        Gets a bool value that force this paragraph generates at new page. Default is false.(for pdf
        generation)
        """
        return self.get_java_object().isInNewPage()

    def setInNewPage(self, value):
        """!
        Sets a boolean value that force this paragraph generates at new page. Default is false.(for
        pdf generation)
        """
        self.get_java_object().setInNewPage(value)

    def isInLineParagraph(self):
        """!
        Gets a paragraph is inline. Default is false.(for pdf generation)
        """
        return self.get_java_object().isInLineParagraph()

    def setInLineParagraph(self, value):
        """!
        Sets a paragraph is inline. Default is false.(for pdf generation)
        """
        self.get_java_object().setInLineParagraph(value)

    def getZIndex(self):
        """!
        Gets an int value that indicates the Z-order of the graph. A graph with larger ZIndex will be
        placed over the graph with smaller ZIndex. ZIndex can be negative. Graph with negative ZIndex
        will be placed behind the text in the page.
        """
        return self.get_java_object().getZIndex()

    def setZIndex(self, value):
        """!
        Sets a int value that indicates the Z-order of the graph. A graph with larger ZIndex will be
        placed over the graph with smaller ZIndex. ZIndex can be negative. Graph with negative ZIndex
        will be placed behind the text in the page.
        """
        self.get_java_object().setZIndex(value)

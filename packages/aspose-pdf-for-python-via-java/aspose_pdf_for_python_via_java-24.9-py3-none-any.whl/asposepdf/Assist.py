import jpype


class BaseJavaClass(object):
    java_class_name = None
    java_class = None

    def __init__(self, java_object=None):
        if java_object is not None:
            self.java_object = java_object

    @classmethod
    def get_java_class(cls):
        return cls.java_class

    @classmethod
    def set_java_class(cls, java_class):
        cls.java_class = java_class

    def get_java_object(self):
        return self.java_object

    def set_java_object(self, java_object):
        self.java_object = java_object

    def get_java_class_name(self):
        return self.java_class_name

    def is_null(self):
        return self.java_class.is_null()


class JavaRectangle(BaseJavaClass):
    """!
    A Rectangle specifies an area in a coordinate space that is
    enclosed by the Rectangle object's upper-left point
    in the coordinate space, its width, and its height.
    """

    javaClassName = "java.awt.Rectangle"

    def __init__(self, x, y, width, height):
        """!
        Rectangle constructor.
       @param x The x-coordinate of the upper-left corner of the rectangle.
       @param y The y-coordinate of the upper-left corner of the rectangle.
       @param width The width of the rectangle.
       @param height The height of the rectangle.
        """
        javaRectangle = jpype.JClass(self.javaClassName)
        self.javaClass = javaRectangle(x, y, width, height)
        super().__init__(self.javaClass)

    @staticmethod
    def construct(arg):
        rectangle = JavaRectangle(0, 0, 0, 0)
        rectangle.javaClass = arg
        return rectangle

    def getX(self):
        """!
        Returns the X coordinate of the bounding Rectangle in
        double precision.
        @return the X coordinate of the bounding Rectangle.
        """
        return int(self.get_java_object().getX())

    def getY(self):
        """!
        Returns the Y coordinate of the bounding Rectangle in
       double precision.
        @return the Y coordinate of the bounding Rectangle.
        """
        return int(self.get_java_object().getY())

    def getLeft(self):
        """!
        Gets the x-coordinate of the left edge of self Rectangle class.
        @returns The x-coordinate of the left edge of self Rectangle class.
        """
        return self.getX()

    def getTop(self):
        """!
        Gets the y-coordinate of the top edge of self Rectangle class.
        @returns The y-coordinate of the top edge of self Rectangle class.
        """
        return self.getY()

    def getRight(self):
        """!
        Gets the x-coordinate that is the sum of X and Width property values of self Rectangle class.
        @returns The x-coordinate that is the sum of X and Width of self Rectangle.
        """
        return self.getX() + self.getWidth()

    def getBottom(self):
        """!
        Gets the y-coordinate that is the sum of the Y and Height property values of self Rectangle class.
        @returns The y-coordinate that is the sum of Y and Height of self Rectangle.
        """
        return self.getY() + self.getHeight()

    def getWidth(self):
        """!
        Returns the width of the bounding Rectangle in
        double precision.
        @return the width of the bounding Rectangle.
        """
        return int(self.get_java_object().getWidth())

    def getHeight(self):
        """!
        Returns the height of the bounding Rectangle in
        double precision.
        @return the height of the bounding Rectangle.
        """
        return int(self.get_java_object().getHeight())

    def toString(self):
        return str(int(self.getX())) + ',' + str(int(self.getY())) + ',' + str(int(self.getWidth())) + ',' + str(
            int(self.getHeight()))

    def equals(self, obj):
        return self.get_java_object().equals(obj.get_java_object())

    def intersectsWithInclusive(self, rectangle):
        """!
       Determines if self rectangle intersects with rect.
       @param rectangle
       @returns {boolean
        """
        return not ((self.getLeft() > rectangle.getRight()) | (self.getRight() < rectangle.getLeft()) |
                    (self.getTop() > rectangle.getBottom()) | (self.getBottom() < rectangle.getTop()))

    @staticmethod
    def intersect(a, b):
        """!
        Intersect Shared Method
        Produces a new Rectangle by intersecting 2 existing
        Rectangles. Returns null if there is no    intersection.
        """
        if (not a.intersectsWithInclusive(b)):
            return JavaRectangle(0, 0, 0, 0)

        return JavaRectangle.fromLTRB(max(a.getLeft(), b.getLeft()),
                                      max(a.getTop(), b.getTop()),
                                      min(a.getRight(), b.getRight()),
                                      min(a.getBottom(), b.getBottom()))

    @staticmethod
    def fromLTRB(left, top, right, bottom):
        """!
        FromLTRB Shared Method
        Produces a Rectangle class from left, top, right,
        and bottom coordinates.
        """
        return JavaRectangle(left, top, right - left, bottom - top)

    def isEmpty(self):
        return (self.getWidth() <= 0) | (self.getHeight() <= 0)


class Point(BaseJavaClass):
    javaClassName = "java.awt.Point"

    def __init__(self, x, y):
        javaRectangle = jpype.JClass(Point.javaClassName)
        self.javaClass = javaRectangle(int(x), int(y))
        super().__init__(self.javaClass)

    @staticmethod
    def construct(arg):
        point = Point(0, 0)
        point.javaClass = arg
        return point

    def getX(self):
        """!
        The X coordinate of this <code>Point</code>.
        If no X coordinate is set it will default to 0.
        """
        return int(self.get_java_object().getX())

    def getY(self):
        """!
        The Y coordinate of this <code>Point</code>.
         If no Y coordinate is set it will default to 0.
        """
        return int(self.get_java_object().getY())

    def setX(self, x):
        """!
        The Y coordinate of this <code>Point</code>.
         If no Y coordinate is set it will defaultto 0.
        """
        self.get_java_object().x = x

    def setY(self, y):
        """!
        The Y coordinate of this <code>Point</code>.
         If no Y coordinate is set it will default to 0.
        """
        self.get_java_object().y = y

    def toString(self):
        return self.getX() + ',' + self.getY()

    def equals(self, obj):
        return self.get_java_object().equals(obj.get_java_object())


class PdfException(Exception):

    @staticmethod
    def MAX_LINES():
        return 4

    def __init__(self, exc):
        self.message = None
        super().__init__(self, exc)
        if isinstance(exc, str):
            self.setMessage(str(exc))
            return

        exc_message = 'Exception occurred in file:line\n'

        self.setMessage(exc_message)

    def setMessage(self, message):
        self.message = message

    def getMessage(self):
        return self.message

class PointOutOfCanvas(Exception):
    pass


class Canvas(object):
    def __init__(self, width, height, point_factory):
        assert(width > 0 and height > 0)
        self._width = width
        self._height = height
        self._matrix = [[point_factory.create_point(x, y) for y in xrange(height)] for x in xrange(width)]

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def point(self, x, y):
        if x < 0 or x >= self.width:
            raise PointOutOfCanvas
        if y < 0 or y >= self.height:
            raise PointOutOfCanvas
        return self._matrix[x][y]

    def horizontal_line(self, x1, x2, y):
        """
        Returns the list of points between (x1, y) and (x2, y)
        """
        return [self.point(x, y) for x in (xrange(x1, x2 + 1) if x2 >= x1 else xrange(x2, x1 + 1))]

    def vertical_line(self, x, y1, y2):
        """
        Returns the list of points between (x, y1) and (x, y2)
        """
        return [self.point(x, y) for y in (xrange(y1, y2 + 1) if y2 >= y1 else xrange(y2, y1 + 1))]

    def connected(self, x, y):
        """
        Returns the set of points of the area connected to (x, y)
        """
        def func(color, visited, linked, x1, y1):
            try:
                point = self.point(x1, y1)
            except PointOutOfCanvas:
                pass
            else:
                if point not in visited:
                    visited.add(point)
                    if point.color == color:
                        linked.add(point)
                        func(color, visited, linked, x1 - 1, y1)
                        func(color, visited, linked, x1 + 1, y1)
                        func(color, visited, linked, x1, y1 - 1)
                        func(color, visited, linked, x1, y1 + 1)
            return linked

        return func(self.point(x, y).color, set(), set(), x, y)


class PointFactory(object):
    def __init__(self, default_color, palette):
        assert(default_color in palette)
        self.default_color = default_color
        self.palette = palette

    def create_point(self, x, y):
        """Creates a new point"""
        return Point(x, y, self.default_color, palette=self.palette)


class Point(object):
    def __init__(self, x, y, color, palette):
        self._x = x
        self._y = y
        self._palette = palette
        self.color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if value not in self._palette:
            raise ValueError("Unknown color")
        self._color = value

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class Painter(object):
    def __init__(self, canvas):
        self._canvas = canvas

    def draw_horizontal_line(self, x1, x2, y, color):
        """
        Paints the line between (x1, y) and (x2, y)
        """
        for point in self._canvas.horizontal_line(x1=x1, x2=x2, y=y):
            point.color = color

    def draw_vertical_line(self, x, y1, y2, color):
        """
        Paints the line between (x, y1) and (x, y2)
        """
        for point in self._canvas.vertical_line(x=x, y1=y1, y2=y2):
            point.color = color

    def draw_rectangle(self, x1, y1, x2, y2, color):
        """
        Paints the border of the rectangle with corners in (x1, y1) and (x2, y2)
        """
        self.draw_horizontal_line(x1=x1, x2=x2, y=y1, color=color)
        self.draw_horizontal_line(x1=x1, x2=x2, y=y2, color=color)
        self.draw_vertical_line(x=x1, y1=y1, y2=y2, color=color)
        self.draw_vertical_line(x=x2, y1=y1, y2=y2, color=color)

    def bucket_fill(self, x, y, color):
        """
        Paints the area connected to (x, y)
        """
        for point in self._canvas.connected(x=x, y=y):
            point.color = color

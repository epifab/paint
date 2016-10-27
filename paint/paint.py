class PointOutOfCanvas(Exception):
    pass


class Canvas(object):
    def __init__(self, x, y, point_factory):
        assert(x > 0)
        assert(y > 0)
        self._matrix = [[point_factory.create_point(i, j) for j in xrange(y)] for i in xrange(x)]

    def point(self, x, y):
        try:
            return self._matrix[x][y]
        except IndexError:
            raise PointOutOfCanvas("Point out of canvas")

    def horizontal_line(self, x1, x2, y):
        return [self.point(x, y) for x in (xrange(x1, x2 + 1) if x2 >= x1 else xrange(x2, x1 + 1))]

    def vertical_line(self, x, y1, y2):
        return [self.point(x, y) for y in (xrange(y1, y2 + 1) if y2 >= y1 else xrange(y2, y1 + 1))]


class PointFactory(object):
    def __init__(self, default_color, palette):
        assert(default_color in palette)
        self.default_color = default_color
        self.palette = palette

    def create_point(self, x, y):
        return Point(x, y, self.default_color, palette=self.palette)


class Point(object):
    def __init__(self, x, y, color, palette):
        self._x = x
        self._y = y
        self._color = color
        self._palette = palette

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if value not in self._palette:
            raise ValueError("Unknown colour")
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
        for point in self._canvas.horizontal_line(x1=x1, x2=x2, y=y):
            point.color = color

    def draw_vertical_line(self, x, y1, y2, color):
        for point in self._canvas.vertical_line(x=x, y1=y1, y2=y2):
            point.color = color

    def draw_rectangle(self, x1, y1, x2, y2, color):
        self.draw_horizontal_line(x1=x1, x2=x2, y=y1, color=color)
        self.draw_horizontal_line(x1=x1, x2=x2, y=y2, color=color)
        self.draw_vertical_line(x=x1, y1=y1, y2=y2, color=color)
        self.draw_vertical_line(x=x2, y1=y1, y2=y2, color=color)

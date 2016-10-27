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

class PointFactoryInterface(object):
    def create_point(self, x, y, color=None):
        raise NotImplemented


class PointFactory(PointFactoryInterface):
    def __init__(self, default_color):
        self.default_color = default_color
        self.points = {}

    def create_point(self, x, y, color=None):
        """Creates a new point"""
        color = self.default_color if color is None else color
        if color not in self.points:
            self.points[color] = Point(color)
        return self.points[color]


class Point(object):
    def __init__(self, color):
        self._color = color

    @property
    def color(self):
        return self._color

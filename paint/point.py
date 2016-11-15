from collections import namedtuple


Point = namedtuple('Point', ('x', 'y', 'color'))


class PointFactory(object):
    def __init__(self, default_color):
        self.default_color = default_color
        self.points = {}

    def create_point(self, x, y, color=None):
        """Creates a new point"""
        color = self.default_color if color is None else color
        return Point(x, y, color)

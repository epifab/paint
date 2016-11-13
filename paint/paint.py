class PointOutOfCanvas(Exception):
    pass


class BaseCanvas(object):
    @property
    def width(self):
        raise NotImplementedError

    @property
    def height(self):
        raise NotImplementedError

    def point(self, x, y):
        raise NotImplementedError

    def exists(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def _point_coordinate(self, x, y):
        if not self.exists(x, y):
            raise PointOutOfCanvas
        return x, y

    def horizontal_line(self, x, y, xx):
        """
        Returns the list of points between (x1, y) and (x2, y)
        """
        if x > xx:
            x, xx = xx, x
        return {self._point_coordinate(x, y) for x in (range(x, xx + 1))}

    def vertical_line(self, x, y, yy):
        """
        Returns the list of points between (x, y1) and (x, y2)
        """
        if y > yy:
            y, yy = yy, y
        return {self._point_coordinate(x, y) for y in (range(y, yy + 1))}

    def line(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return {self._point_coordinate(x1, y1)}
        elif x1 == x2:
            return self.vertical_line(x=x1, y=y1, yy=y2)
        elif y1 == y2:
            return self.horizontal_line(x=x1, y=y1, xx=x2)

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        m = float(y2 - y1) / float(x2 - x1)
        return {
            self._point_coordinate(x, int(round((m * (x - x1)) + y1)))
            for x in range(x1, x2 + 1)
        }

    def uniform_area(self, x, y):
        """
        Returns the set of points of the area connected to (x, y)
        """
        def loop(color, stack, visited, linked):
            while stack:
                x1, y1 = stack.pop()
                try:
                    if self.point(x1, y1).color == color:
                        linked.add((x1, y1))
                        nearby = [
                            (x1 - 1, y1),
                            (x1 + 1, y1),
                            (x1, y1 - 1),
                            (x1, y1 + 1)
                        ]

                        for p2 in nearby:
                            if p2 not in visited:
                                visited.add(p2)
                                stack.add(p2)
                except PointOutOfCanvas:
                    pass

            return linked

        return loop(self.point(x, y).color, {(x, y)}, set(), set())


class Canvas(BaseCanvas):
    def __init__(self, width, height, point_factory):
        assert(width > 0)
        assert(height > 0)
        self._width = width
        self._height = height
        self._matrix = [[point_factory.create_point(x, y) for y in range(height)] for x in range(width)]

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def point(self, x, y):
        if not self.exists(x, y):
            raise PointOutOfCanvas
        return self._matrix[x][y]


class EditedCanvas(BaseCanvas):
    def __init__(self, canvas, delta):
        self.original_canvas = canvas
        self.delta = delta

    @property
    def height(self):
        return self.original_canvas.height

    @property
    def width(self):
        return self.original_canvas.width

    def point(self, x, y):
        if (x, y) in self.delta:
            return self.delta[(x, y)]
        else:
            return self.original_canvas.point(x, y)


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


class Painter(object):
    def __init__(self, point_factory):
        self._point_factory = point_factory

    def draw_line(self, canvas, x1, y1, x2, y2, color):
        """
        Paints the line between (x1, y1) and (x2, y2)
        """
        return EditedCanvas(
            canvas=canvas,
            delta={
                (x, y): self._point_factory.create_point(x, y, color)
                for x, y in canvas.line(x1=x1, y1=y1, x2=x2, y2=y2)
            }
        )

    def draw_rectangle(self, canvas, x1, y1, x2, y2, color):
        """
        Paints the border of the rectangle with corners in (x1, y1) and (x2, y2)
        """
        return EditedCanvas(
            canvas=canvas,
            delta={
                (x, y): self._point_factory.create_point(x, y, color)
                for x, y in
                    canvas.line(x1, y1, x2, y1) |
                    canvas.line(x2, y1, x2, y2) |
                    canvas.line(x2, y2, x1, y2) |
                    canvas.line(x1, y2, x1, y1)
            }
        )

    def bucket_fill(self, canvas, x, y, color):
        """
        Paints the area connected to (x, y)
        """
        return EditedCanvas(
            canvas=canvas,
            delta={
                (x, y): self._point_factory.create_point(x, y, color)
                for x, y in canvas.uniform_area(x, y)
            }
        )

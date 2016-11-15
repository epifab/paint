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
        return 0 <= int(x) < self.width and 0 <= int(y) < self.height

    def coordinate(self, x, y):
        if not self.exists(x, y):
            raise PointOutOfCanvas
        return x, y

    def range(self, a, b):
        step = 1 if a < b else -1
        while a != b:
            yield a
            a += step
        yield b

    def line(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            # Single point
            yield self.coordinate(x1, y1)
        elif x1 == x2:
            # Vertical line
            for y in self.range(y1, y2):
                yield self.coordinate(x1, y)
        elif y1 == y2:
            # Horizontal line
            for x in self.range(x1, x2):
                yield self.coordinate(x, y1)
        else:
            # Diagonal line
            m = float(y2 - y1) / float(x2 - x1)
            if abs(x2 - x1) > abs(y2 - y1):
                for x in self.range(x1, x2):
                    y = int(round(float(x - x1) * m)) + y1
                    yield self.coordinate(x, y)
            else:
                for y in self.range(y1, y2):
                    x = int(round(float(y - y1) / m)) + x1
                    yield self.coordinate(x, y)

    def rectangle(self, x1, y1, x2, y2):
        return self.polygon((x1, y1), (x2, y1), (x2, y2), (x1, y2))

    def triangle(self, x1, y1, x2, y2, x3, y3):
        return self.polygon((x1, y1), (x2, y2), (x3, y3))

    def polygon(self, *args):
        assert len(args) >= 3, "A polygon is made of at least 3 points"

        points = iter(args)

        first_point = next(points)

        p1 = first_point

        for p2 in points:
            for p in self.line(p1[0], p1[1], p2[0], p2[1]):
                yield p
            p1 = p2

        for p in self.line(p1[0], p1[1], first_point[0], first_point[1]):
            yield p

    def uniform_area(self, x, y):
        """
        Returns the set of points of the area connected to (x, y)
        """
        color = self.point(x, y).color
        stack = {(x, y)}
        visited = set()

        while stack:
            x1, y1 = stack.pop()
            try:
                if self.point(x1, y1).color == color:
                    yield x1, y1

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


class Canvas(BaseCanvas):
    def __init__(self, width, height, point_factory):
        assert width > 0 and height > 0, "Invalid width or height"
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
                for x, y in canvas.rectangle(x1, y1, x2, y2)
            }
        )

    def draw_polygon(self, canvas, color, *args):
        """
        Draws a polygon
        """
        return EditedCanvas(
            canvas=canvas,
            delta={
                (x, y): self._point_factory.create_point(x, y, color)
                for x, y in canvas.polygon(*args)
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

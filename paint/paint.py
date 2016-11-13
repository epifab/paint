class PointOutOfCanvas(Exception):
    pass


class Canvas(object):
    def __init__(self, width, height, point_factory):
        assert(width > 0 and height > 0)
        self._width = width
        self._height = height
        self._matrix = [[point_factory.create_point(x, y) for y in range(height)] for x in range(width)]

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def exists(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def point(self, x, y):
        if not self.exists(x, y):
            raise PointOutOfCanvas
        return self._matrix[x][y]

    def horizontal_line(self, x, y, xx):
        """
        Returns the list of points between (x1, y) and (x2, y)
        """
        if x > xx:
            x, xx = xx, x
        return [self.point(x, y) for x in (range(x, xx + 1))]

    def vertical_line(self, x, y, yy):
        """
        Returns the list of points between (x, y1) and (x, y2)
        """
        if y > yy:
            y, yy = yy, y
        return [self.point(x, y) for y in (range(y, yy + 1))]

    def line(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return [self.point(x1, y1)]
        elif x1 == x2:
            return self.vertical_line(x=x1, y=y1, yy=y2)
        elif y1 == y2:
            return self.horizontal_line(x=x1, y=y1, xx=x2)

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        m = float(y2 - y1) / float(x2 - x1)
        return [
            self.point(x, int(round((m * (x - x1)) + y1)))
            for x in range(x1, x2 + 1)
        ]

    def uniform_area(self, x, y):
        """
        Returns the set of points of the area connected to (x, y)
        """
        visited = set()
        linked = set()
        stack = []

        point = self.point(x, y)
        color = point.color
        stack.append(point)

        while stack:
            point = stack.pop()
            visited.add(point)
            if point.color == color:
                linked.add(point)
                nearby = [
                    (point.x - 1, point.y),
                    (point.x + 1, point.y),
                    (point.x, point.y - 1),
                    (point.x, point.y + 1),
                ]
                for x2, y2 in nearby:
                    try:
                        point_nearby = self.point(x2, y2)
                        if point_nearby not in visited:
                            stack.append(point_nearby)
                    except PointOutOfCanvas:
                        pass

        return linked


class PointFactoryInterface(object):
    def create_point(self, x, y, color=None):
        raise NotImplemented


class PointFactory(PointFactoryInterface):
    def __init__(self, default_color):
        self.default_color = default_color

    def create_point(self, x, y, color=None):
        """Creates a new point"""
        return Point(x, y, self.default_color if color is None else color)


class DeltaPointFactory(PointFactoryInterface):
    def __init__(self, canvas, delta, base_factory):
        self.canvas = canvas
        self.delta = {
            (point.x, point.y): point
            for point in delta
        }
        self.base_factory = base_factory

    def create_point(self, x, y, color=None):
        if color is not None:
            return self.base_factory.create_point(x, y, color)
        elif (x, y) in self.delta:
            return self.delta[(x, y)]
        try:
            return self.canvas.point(x, y)
        except PointOutOfCanvas:
            return self.base_factory.create_point(x, y)


class Point(object):
    def __init__(self, x, y, color):
        self._x = x
        self._y = y
        self._color = color

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def color(self):
        return self._color


class Painter(object):
    def __init__(self, point_factory):
        self._point_factory = point_factory

    def _create_canvas(self, canvas, delta):
        return Canvas(
            canvas.width,
            canvas.height,
            DeltaPointFactory(canvas, delta, self._point_factory)
        )

    def draw_line(self, canvas, x1, y1, x2, y2, color):
        """
        Paints the line between (x1, y1) and (x2, y2)
        """
        return self._create_canvas(
            canvas=canvas,
            delta=[
                self._point_factory.create_point(point.x, point.y, color)
                for point in canvas.line(x1=x1, y1=y1, x2=x2, y2=y2)
            ]
        )

    def draw_rectangle(self, canvas, x1, y1, x2, y2, color):
        """
        Paints the border of the rectangle with corners in (x1, y1) and (x2, y2)
        """
        return self._create_canvas(
            canvas=canvas,
            delta=[
                self._point_factory.create_point(point.x, point.y, color)
                for point in
                    canvas.line(x1, y1, x2, y1) +
                    canvas.line(x2, y1, x2, y2) +
                    canvas.line(x2, y2, x1, y2) +
                    canvas.line(x1, y2, x1, y1)
            ]
        )

    def bucket_fill(self, canvas, x, y, color):
        """
        Paints the area connected to (x, y)
        """
        return self._create_canvas(
            canvas=canvas,
            delta=[
                self._point_factory.create_point(point.x, point.y, color)
                for point in canvas.uniform_area(x, y)
            ]
        )

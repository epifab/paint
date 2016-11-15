from paint import *
import time
import unittest
from unittest import mock


def timer(func):
    def run(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            print("-" * 80)
            print("Function: {}".format(func.__name__))
            print("Elapsed: {}".format(round(time.time() - start, 3)))
            print("-" * 80)
    return run


class CanvasStub(BaseCanvas):
    def __init__(self, width, height, get_point=lambda x, y: Point("{}-{}".format(x, y))):
        self._width = width
        self._height = height
        self._get_point = get_point

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def point(self, x, y):
        if not self.exists(x, y):
            raise PointOutOfCanvas
        return self._get_point(x, y)


class PointMock(Point):
    def set_color(self, color):
        self._color = color


class CanvasTests(unittest.TestCase):
    def test_constructor_with_non_positive_x_throws_exception(self):
        self.assertRaises(AssertionError, Canvas, -1, 2, mock.Mock())
        self.assertRaises(AssertionError, Canvas, 0, 2, mock.Mock())

    def test_constructor_with_non_positive_y_throws_exception(self):
        self.assertRaises(AssertionError, Canvas, 1, -1, mock.Mock())
        self.assertRaises(AssertionError, Canvas, 1, 0, mock.Mock())

    def test_point_in_range(self):
        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: (x, y)
        canvas = Canvas(10, 8, point_factory_mock)
        self.assertEqual((3, 4), canvas.point(3, 4))
        self.assertEqual((0, 0), canvas.point(0, 0))
        self.assertEqual((0, 7), canvas.point(0, 7))
        self.assertEqual((9, 0), canvas.point(9, 0))
        self.assertEqual((9, 7), canvas.point(9, 7))

    def test_point_out_of_range(self):
        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: (x, y)
        canvas = Canvas(10, 8, point_factory_mock)
        self.assertRaises(PointOutOfCanvas, canvas.point, 13, 12)
        self.assertRaises(PointOutOfCanvas, canvas.point, 10, 0)
        self.assertRaises(PointOutOfCanvas, canvas.point, 0, 8)

    def test_point_negative_x(self):
        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: (x, y)
        canvas = Canvas(10, 8, point_factory_mock)
        self.assertRaises(PointOutOfCanvas, canvas.point, -2, 2)

    def test_point_negative_y(self):
        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: (x, y)
        canvas = Canvas(10, 8, point_factory_mock)
        self.assertRaises(PointOutOfCanvas, canvas.point, 2, -2)

    def test_horizontal_line(self):
        canvas = CanvasStub(10, 8)
        expected_points = {
            (2, 3),
            (3, 3),
            (4, 3),
            (5, 3)
        }
        self.assertEqual(expected_points, set(canvas.line(x1=2, y1=3, x2=5, y2=3)))

    def test_horizontal_line_when_out_of_range_throws_exception(self):
        width = 10
        height = 8
        canvas = CanvasStub(width, height)
        line = canvas.line(x1=-1, y1=2, x2=4, y2=3)
        self.assertRaises(PointOutOfCanvas, set, line)
        line = canvas.line(x1=width, y1=2, x2=4, y2=3)
        self.assertRaises(PointOutOfCanvas, set, line)
        line = canvas.line(x1=2, y1=-1, x2=4, y2=3)
        self.assertRaises(PointOutOfCanvas, set, line)
        line = canvas.line(x1=2, y1=height, x2=4, y2=3)
        self.assertRaises(PointOutOfCanvas, set, line)

    def test_vertical_line(self):
        canvas = CanvasStub(10, 8)
        expected_points = {
            (3, 2),
            (3, 3),
            (3, 4),
            (3, 5)
        }
        self.assertEqual(expected_points, set(canvas.line(x1=3, y1=2, x2=3, y2=5)))
        self.assertEqual(expected_points, set(canvas.line(x1=3, y1=5, x2=3, y2=2)))

    def test_line_single_point(self):
        canvas = CanvasStub(10, 8)
        expected_points = {(3, 2)}
        self.assertEqual(expected_points, set(canvas.line(x1=3, y1=2, x2=3, y2=2)))

    def test_diagonal_line(self):
        width = 10
        height = 10

        canvas = CanvasStub(width, height)

        #   0 1 2 3 4 5
        # 0
        # 1   x
        # 2     x
        # 3       x
        # 4
        # 5
        self.assertEqual({(1, 1), (2, 2), (3, 3)}, set(canvas.line(1, 1, 3, 3)))
        self.assertEqual({(1, 1), (2, 2), (3, 3)}, set(canvas.line(3, 3, 1, 1)))

        #   0 1 2 3 4 5
        # 0
        # 1       x
        # 2     x
        # 3   x
        # 4
        # 5
        self.assertEqual({(3, 1), (2, 2), (1, 3)}, set(canvas.line(3, 1, 1, 3)))
        self.assertEqual({(3, 1), (2, 2), (1, 3)}, set(canvas.line(1, 3, 3, 1)))

        #   0 1 2 3 4 5
        # 0
        # 1   x
        # 2   x
        # 3     x
        # 4     x
        # 5
        self.assertEqual({(1, 1), (1, 2), (2, 3), (2, 4)}, set(canvas.line(1, 1, 2, 4)))
        self.assertEqual({(1, 1), (1, 2), (2, 3), (2, 4)}, set(canvas.line(2, 4, 1, 1)))

        #   0 1 2 3 4 5
        # 0
        # 1   x x
        # 2       x x
        # 3
        # 4
        # 5
        self.assertEqual({(1, 1), (2, 1), (3, 2), (4, 2)}, set(canvas.line(1, 1, 4, 2)))
        self.assertEqual({(1, 1), (2, 1), (3, 2), (4, 2)}, set(canvas.line(4, 2, 1, 1)))

    def test_uniform_area_uniform_canvas(self):
        # ----------
        # ----------
        # ----------
        # ----------
        # ----------
        # ----------
        width = 10
        height = 6

        point_mock = Point('-')
        expected_points = {(x, y) for x in range(width) for y in range(height)}

        canvas = CanvasStub(width, height, lambda x, y: point_mock)

        self.assertSetEqual(expected_points, set(canvas.uniform_area(2, 2)))

    @timer
    def test_uniform_area_large_canvas(self):
        # self.skipTest("Takes several seconds to bucket fill a million points canvas")
        width = 1000
        height = 1000

        point_mock = Point('-')
        expected_points = {(x, y) for x in range(width) for y in range(height)}

        canvas = CanvasStub(width, height, lambda x, y: point_mock)

        self.assertSetEqual(expected_points, set(canvas.uniform_area(2, 2)))

    def test_uniform_area_isolated_point(self):
        # ----------
        # ----------
        # -----X----
        # ----------
        # ----------
        # ----------

        width = 10
        height = 6

        point_mocks = [[PointMock('-') for _ in range(height)] for _ in range(width)]
        point_mocks[3][3].set_color('X')

        canvas = CanvasStub(width, height, lambda x, y: point_mocks[x][y])

        expected_points = {
            (3, 3),
        }
        self.assertSetEqual(expected_points, set(canvas.uniform_area(3, 3)))

    def test_uniform_area_vertically_split_canvas(self):
        # -X--
        # -X--
        # -X--
        # -X--

        width = 4
        height = 4

        point_mocks = [[PointMock('-') for _ in range(height)] for _ in range(width)]
        point_mocks[1][0].set_color('X')
        point_mocks[1][1].set_color('X')
        point_mocks[1][2].set_color('X')
        point_mocks[1][3].set_color('X')

        canvas = CanvasStub(width, height, lambda x, y: point_mocks[x][y])

        expected_points = {
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
        }
        self.assertSetEqual(expected_points, set(canvas.uniform_area(0, 0)))

    def test_uniform_area_horizontally_split_canvas(self):
        # ----
        # XXXX
        # ----
        # ----

        width = 4
        height = 4

        point_mocks = [[PointMock('-') for _ in range(height)] for _ in range(width)]
        point_mocks[0][1].set_color('X')
        point_mocks[1][1].set_color('X')
        point_mocks[2][1].set_color('X')
        point_mocks[3][1].set_color('X')

        canvas = CanvasStub(width, height, lambda x, y: point_mocks[x][y])

        expected_points = {
            (0, 0),
            (1, 0),
            (2, 0),
            (3, 0),
        }
        self.assertSetEqual(expected_points, set(canvas.uniform_area(0, 0)))

    def test_uniform_area_happy_test(self):
        # --------X-
        # --------X-
        # -----X----
        # ---XXX----
        # ----XXXX--
        # ----------

        width = 10
        height = 6

        point_mocks = [[PointMock('-') for _ in range(height)] for _ in range(width)]
        point_mocks[8][0].set_color('X')
        point_mocks[8][1].set_color('X')
        point_mocks[5][2].set_color('X')
        point_mocks[3][3].set_color('X')
        point_mocks[4][3].set_color('X')
        point_mocks[5][3].set_color('X')
        point_mocks[4][4].set_color('X')
        point_mocks[5][4].set_color('X')
        point_mocks[6][4].set_color('X')

        canvas = CanvasStub(width, height, lambda x, y: point_mocks[x][y])

        expected_points = {
            (5, 2),
            (3, 3),
            (4, 3),
            (5, 3),
            (4, 4),
            (5, 4),
            (6, 4),
        }
        self.assertSetEqual(expected_points, set(canvas.uniform_area(3, 3)))


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


class PointDummyFactory:
    def create_point(self, x, y):
        return Point(x, y, None)


class PointColorMatrixFactory(PointDummyFactory):
    def __init__(self, color_matrix=None):
        self._color_matrix = color_matrix

    def create_point(self, x, y):
        return Point(x, y, self._color_matrix[y][x]) if self._color_matrix else Point(x, y, None)


class CanvasStub(Canvas):
    def __init__(self, width, height, factory=PointDummyFactory()):
        super().__init__(width, height, factory)


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
        self.assertEqual(expected_points, set((point.x, point.y) for point in canvas.line(x1=2, y1=3, x2=5, y2=3)))

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
        self.assertEqual(expected_points, set((point.x, point.y) for point in canvas.line(x1=3, y1=2, x2=3, y2=5)))
        self.assertEqual(expected_points, set((point.x, point.y) for point in canvas.line(x1=3, y1=5, x2=3, y2=2)))

    def test_line_single_point(self):
        canvas = CanvasStub(10, 8)
        expected_points = {(3, 2)}
        self.assertEqual(expected_points, set((point.x, point.y) for point in canvas.line(x1=3, y1=2, x2=3, y2=2)))

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
        self.assertEqual({(1, 1), (2, 2), (3, 3)}, set((point.x, point.y) for point in canvas.line(1, 1, 3, 3)))
        self.assertEqual({(1, 1), (2, 2), (3, 3)}, set((point.x, point.y) for point in canvas.line(3, 3, 1, 1)))

        #   0 1 2 3 4 5
        # 0
        # 1       x
        # 2     x
        # 3   x
        # 4
        # 5
        self.assertEqual({(3, 1), (2, 2), (1, 3)}, set((point.x, point.y) for point in canvas.line(3, 1, 1, 3)))
        self.assertEqual({(3, 1), (2, 2), (1, 3)}, set((point.x, point.y) for point in canvas.line(1, 3, 3, 1)))

        #   0 1 2 3 4 5
        # 0
        # 1   x
        # 2   x
        # 3     x
        # 4     x
        # 5
        self.assertEqual({(1, 1), (1, 2), (2, 3), (2, 4)}, set((point.x, point.y) for point in canvas.line(1, 1, 2, 4)))
        self.assertEqual({(1, 1), (1, 2), (2, 3), (2, 4)}, set((point.x, point.y) for point in canvas.line(2, 4, 1, 1)))

        #   0 1 2 3 4 5
        # 0
        # 1   x x
        # 2       x x
        # 3
        # 4
        # 5
        self.assertEqual({(1, 1), (2, 1), (3, 2), (4, 2)}, set((point.x, point.y) for point in canvas.line(1, 1, 4, 2)))
        self.assertEqual({(1, 1), (2, 1), (3, 2), (4, 2)}, set((point.x, point.y) for point in canvas.line(4, 2, 1, 1)))

    def test_uniform_area_uniform_canvas(self):
        width = 10
        height = 6

        expected_points = {Point(x, y, '-') for x in range(width) for y in range(height)}

        canvas = CanvasStub(width, height, factory=PointColorMatrixFactory([
            "----------",
            "----------",
            "----------",
            "----------",
            "----------",
            "----------",
        ]))

        self.assertSetEqual(expected_points, set(canvas.uniform_area(2, 2)))

    @timer
    def test_uniform_area_large_canvas(self):
        # self.skipTest("Takes several seconds to bucket fill a million points canvas")
        width = 1000
        height = 1000

        canvas = CanvasStub(width, height)
        area = canvas.uniform_area(2, 2)

        self.assertEqual(1000000, len(set(area)))

    def test_uniform_area_isolated_point(self):
        width = 10
        height = 6

        canvas = CanvasStub(width, height, factory=PointColorMatrixFactory([
            "----------",
            "----------",
            "-----X----",
            "----------",
            "----------",
            "----------",
        ]))

        expected_points = {(5, 2),}
        self.assertSetEqual(expected_points, set((p.x, p.y) for p in canvas.uniform_area(5, 2)))

    def test_uniform_area_happy_test(self):
        width = 10
        height = 6

        canvas = CanvasStub(width, height, factory=PointColorMatrixFactory([
            "--------X-",
            "--------X-",
            "-----X----",
            "---XXX----",
            "----XXXX--",
            "----------",
        ]))

        expected_points = {
            (5, 2),
            (3, 3),
            (4, 3),
            (5, 3),
            (4, 4),
            (5, 4),
            (6, 4),
            (7, 4),
        }
        self.assertSetEqual(expected_points, set((p.x, p.y) for p in canvas.uniform_area(3, 3)))


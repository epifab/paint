from paint import *
import unittest
from unittest import mock


class CanvasTests(unittest.TestCase):
    class PointMock:
        def __init__(self, x, y, color):
            self.x = x
            self.y = y
            self.color = color

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
        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: (x, y)
        canvas = Canvas(10, 8, point_factory_mock)
        expected_points = [
            (2, 3),
            (3, 3),
            (4, 3),
            (5, 3)
        ]
        self.assertListEqual(expected_points, canvas.horizontal_line(x=2, xx=5, y=3))

    def test_horizontal_line_single_point(self):
        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: (x, y)
        canvas = Canvas(10, 8, point_factory_mock)
        expected_points = [(2, 3)]
        self.assertListEqual(expected_points, canvas.horizontal_line(x=2, xx=2, y=3))

    def test_horizontal_line_when_out_of_range_throws_exception(self):
        width = 10
        height = 8
        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: (x, y)
        canvas = Canvas(10, 8, point_factory_mock)
        self.assertRaises(PointOutOfCanvas, canvas.horizontal_line, x=-1, y=3, xx=4)
        self.assertRaises(PointOutOfCanvas, canvas.horizontal_line, x=width, y=3, xx=4)
        self.assertRaises(PointOutOfCanvas, canvas.horizontal_line, x=2, y=3, xx=-1)
        self.assertRaises(PointOutOfCanvas, canvas.horizontal_line, x=2, y=3, xx=width)
        self.assertRaises(PointOutOfCanvas, canvas.horizontal_line, x=2, y=-1, xx=2)
        self.assertRaises(PointOutOfCanvas, canvas.horizontal_line, x=2, y=height, xx=2)

    def test_vertical_line(self):
        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: (x, y)
        canvas = Canvas(10, 8, point_factory_mock)
        expected_points = [
            (3, 2),
            (3, 3),
            (3, 4),
            (3, 5)
        ]
        self.assertListEqual(expected_points, canvas.vertical_line(x=3, y=2, yy=5))

    def test_vertical_line_single_point(self):
        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: (x, y)
        canvas = Canvas(10, 8, point_factory_mock)
        expected_points = [(3, 2)]
        self.assertListEqual(expected_points, canvas.vertical_line(x=3, y=2, yy=2))

    def test_vertical_line_when_out_of_range_throws_exception(self):
        width = 10
        height = 8
        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: (x, y)
        canvas = Canvas(10, 8, point_factory_mock)
        self.assertRaises(PointOutOfCanvas, canvas.vertical_line, -1, 2, 4)
        self.assertRaises(PointOutOfCanvas, canvas.vertical_line, width, 2, 4)
        self.assertRaises(PointOutOfCanvas, canvas.vertical_line, 4, -1, 4)
        self.assertRaises(PointOutOfCanvas, canvas.vertical_line, 4, height, 4)
        self.assertRaises(PointOutOfCanvas, canvas.vertical_line, 4, 2, -1)
        self.assertRaises(PointOutOfCanvas, canvas.vertical_line, 4, 2, height)

    def test_uniform_area_uniform_canvas(self):
        # ----------
        # ----------
        # ----------
        # ----------
        # ----------
        # ----------
        width = 10
        height = 6

        point_mocks = [[CanvasTests.PointMock(x, y, '-') for y in range(height)] for x in range(width)]
        expected_points = set()
        for x in range(width):
            for y in range(height):
                expected_points.add(point_mocks[x][y])

        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: point_mocks[x][y]
        canvas = Canvas(width, height, point_factory_mock)

        self.assertSetEqual(expected_points, canvas.uniform_area(2, 2))

    def test_uniform_area_large_canvas(self):
        self.skipTest("Takes several seconds to bucket fill a million points canvas")

        width = 1000
        height = 1000

        point_mocks = [[CanvasTests.PointMock(x, y, '-') for y in range(height)] for x in range(width)]
        expected_points = set()
        for x in range(width):
            for y in range(height):
                expected_points.add(point_mocks[x][y])

        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: point_mocks[x][y]
        canvas = Canvas(width, height, point_factory_mock)

        self.assertSetEqual(expected_points, canvas.uniform_area(2, 2))

    def test_uniform_area_isolated_point(self):
        # ----------
        # ----------
        # -----X----
        # ----------
        # ----------
        # ----------

        width = 10
        height = 6

        point_mocks = [[CanvasTests.PointMock(x, y, '-') for y in range(height)] for x in range(width)]
        point_mocks[3][3].color = 'X'

        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: point_mocks[x][y]
        canvas = Canvas(width, height, point_factory_mock)

        expected_points = {
            point_mocks[3][3],
        }
        self.assertSetEqual(expected_points, canvas.uniform_area(3, 3))

    def test_uniform_area_vertically_split_canvas(self):
        # -X--
        # -X--
        # -X--
        # -X--

        width = 4
        height = 4

        point_mocks = [[CanvasTests.PointMock(x, y, '-') for y in range(height)] for x in range(width)]
        point_mocks[1][0].color = 'X'
        point_mocks[1][1].color = 'X'
        point_mocks[1][2].color = 'X'
        point_mocks[1][3].color = 'X'

        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: point_mocks[x][y]
        canvas = Canvas(width, height, point_factory_mock)

        expected_points = {
            point_mocks[0][0],
            point_mocks[0][1],
            point_mocks[0][2],
            point_mocks[0][3],
        }
        self.assertSetEqual(expected_points, canvas.uniform_area(0, 0))

    def test_uniform_area_horizontally_split_canvas(self):
        # ----
        # XXXX
        # ----
        # ----

        width = 4
        height = 4

        point_mocks = [[CanvasTests.PointMock(x, y, '-') for y in range(height)] for x in range(width)]
        point_mocks[0][1].color = 'X'
        point_mocks[1][1].color = 'X'
        point_mocks[2][1].color = 'X'
        point_mocks[3][1].color = 'X'

        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: point_mocks[x][y]
        canvas = Canvas(width, height, point_factory_mock)

        expected_points = {
            point_mocks[0][0],
            point_mocks[1][0],
            point_mocks[2][0],
            point_mocks[3][0],
        }
        self.assertSetEqual(expected_points, canvas.uniform_area(0, 0))

    def test_uniform_area_happy_test(self):
        # --------X-
        # --------X-
        # -----X----
        # ---XXX----
        # ----XXXX--
        # ----------

        width = 10
        height = 6

        point_mocks = [[CanvasTests.PointMock(x, y, '-') for y in range(height)] for x in range(width)]
        point_mocks[8][0].color = 'X'
        point_mocks[8][1].color = 'X'
        point_mocks[5][2].color = 'X'
        point_mocks[3][3].color = 'X'
        point_mocks[4][3].color = 'X'
        point_mocks[5][3].color = 'X'
        point_mocks[4][4].color = 'X'
        point_mocks[5][4].color = 'X'
        point_mocks[6][4].color = 'X'

        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: point_mocks[x][y]
        canvas = Canvas(width, height, point_factory_mock)

        expected_points = {
            point_mocks[5][2],
            point_mocks[3][3],
            point_mocks[4][3],
            point_mocks[5][3],
            point_mocks[4][4],
            point_mocks[5][4],
            point_mocks[6][4],
        }
        self.assertSetEqual(expected_points, canvas.uniform_area(3, 3))

    def test_uniform_area_out_of_range_throws_exception(self):
        width = 10
        height = 6

        point_mocks = [[CanvasTests.PointMock(x, y, '-') for y in range(height)] for x in range(width)]

        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: point_mocks[x][y]
        canvas = Canvas(width, height, point_factory_mock)

        self.assertRaises(PointOutOfCanvas, canvas.uniform_area, -1, 3)
        self.assertRaises(PointOutOfCanvas, canvas.uniform_area, width, 3)
        self.assertRaises(PointOutOfCanvas, canvas.uniform_area, 2, -1)
        self.assertRaises(PointOutOfCanvas, canvas.uniform_area, 2, height)

    def test_line(self):
        width = 10
        height = 10

        point_mocks = [[CanvasTests.PointMock(x, y, '-') for y in range(height)] for x in range(width)]

        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: point_mocks[x][y]
        canvas = Canvas(width, height, point_factory_mock)

        self.assertEqual([point_mocks[1][1], point_mocks[2][2], point_mocks[3][3]], canvas.line(1, 1, 3, 3))


class PainterTests(unittest.TestCase):
    def test_draw_line(self):
        expected_canvas = [
            "      ",
            "  XXX ",
            "      ",
        ]

        def line_mock(x1, y1, x2, y2):
            if (x1, y1) == (2, 1) and (x2, y2) == (4, 1):
                return [Point(2, 1, ' '), Point(3, 1, ' '), Point(4, 1, ' ')]
            else:
                raise Exception("Painter shouldn't need to get any other line")

        canvas_mock = mock.Mock()
        canvas_mock.width = 6
        canvas_mock.height = 3
        canvas_mock.point.side_effect = lambda x, y: Point(x, y, ' ')
        canvas_mock.line.side_effect = line_mock

        painter = Painter(PointFactory('-'))
        canvas = painter.draw_line(canvas_mock, x1=2, y1=1, x2=4, y2=1, color='X')

        for y, expected_row in enumerate(expected_canvas):
            for x, expected_point_color in enumerate(expected_row):
                self.assertEqual(expected_point_color, canvas.point(x, y).color)

    def test_draw_rectangle(self):
        expected_canvas = [
            "  XXX ",
            "  X X ",
            "  XXX ",
        ]

        def line_mock(x1, y1, x2, y2):
            if (x1, y1) == (2, 0) and (x2, y2) == (4, 0):
                return [Point(2, 0, ' '), Point(3, 0, ' '), Point(4, 0, ' ')]
            elif (x1, y1) == (4, 0) and (x2, y2) == (4, 2):
                return [Point(4, 0, ' '), Point(4, 1, ' '), Point(4, 2, ' ')]
            elif (x1, y1) == (4, 2) and (x2, y2) == (2, 2):
                return [Point(4, 2, ' '), Point(3, 2, ' '), Point(2, 2, ' ')]
            elif (x1, y1) == (2, 2) and (x2, y2) == (2, 0):
                return [Point(2, 2, ' '), Point(2, 1, ' '), Point(2, 0, ' ')]
            else:
                raise Exception("Painter shouldn't need to get any other line")

        canvas_mock = mock.Mock()
        canvas_mock.width = 6
        canvas_mock.height = 3
        canvas_mock.point.side_effect = lambda x, y: Point(x, y, ' ')
        canvas_mock.line.side_effect = line_mock

        painter = Painter(PointFactory('-'))
        canvas = painter.draw_rectangle(canvas_mock, x1=2, y1=0, x2=4, y2=2, color='X')

        for y, expected_row in enumerate(expected_canvas):
            for x, color in enumerate(expected_row):
                self.assertEqual(color, canvas.point(x, y).color)

    def test_bucket_fill(self):
        expected_canvas = [
            "  XXX ",
            "  XXX ",
            "  XXX ",
        ]

        def uniform_area_mock(x, y):
            if x == 1 and y == 1:
                return [
                    Point(2, 0, 'a'), Point(3, 0, 'a'), Point(4, 0, 'a'),
                    Point(2, 1, 'a'), Point(3, 1, 'a'), Point(4, 1, 'a'),
                    Point(2, 2, 'a'), Point(3, 2, 'a'), Point(4, 2, 'a'),
                ]
            else:
                raise Exception("Painter shouldn't need to get any other area")

        canvas_mock = mock.Mock()
        canvas_mock.width = 6
        canvas_mock.height = 3
        canvas_mock.point.side_effect = lambda x, y: Point(x, y, ' ')
        canvas_mock.uniform_area = uniform_area_mock

        painter = Painter(PointFactory('-'))
        canvas = painter.bucket_fill(canvas_mock, x=1, y=1, color='X')

        for y, expected_row in enumerate(expected_canvas):
            for x, color in enumerate(expected_row):
                self.assertEqual(color, canvas.point(x, y).color)


if __name__ == "__main__":
    unittest.main()

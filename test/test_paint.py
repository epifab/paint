from paint import *
import unittest
import mock


class CanvasTests(unittest.TestCase):
    class PointMock:
        def __init__(self, color):
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
        self.assertEquals((3, 4), canvas.point(3, 4))
        self.assertEquals((0, 0), canvas.point(0, 0))
        self.assertEquals((0, 7), canvas.point(0, 7))
        self.assertEquals((9, 0), canvas.point(9, 0))
        self.assertEquals((9, 7), canvas.point(9, 7))

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
        expeceted_points = [
            (2, 3),
            (3, 3),
            (4, 3),
            (5, 3)
        ]
        self.assertListEqual(expeceted_points, canvas.horizontal_line(x1=2, x2=5, y=3))

    def test_vertical_line(self):
        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: (x, y)
        canvas = Canvas(10, 8, point_factory_mock)
        expeceted_points = [
            (3, 2),
            (3, 3),
            (3, 4),
            (3, 5)
        ]
        self.assertListEqual(expeceted_points, canvas.vertical_line(x=3, y1=2, y2=5))

    def test_connected_uniform_canvas(self):
        # ----------
        # ----------
        # ----------
        # ----------
        # ----------
        # ----------
        width = 10
        height = 6

        point_mocks = [[CanvasTests.PointMock('-') for _ in xrange(height)] for _ in xrange(width)]
        expected_points = set()
        for x in xrange(width):
            for y in xrange(height):
                expected_points.add(point_mocks[x][y])

        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: point_mocks[x][y]
        canvas = Canvas(width, height, point_factory_mock)

        self.assertSetEqual(expected_points, canvas.connected(2, 2))

    def test_connected_isolated_point(self):
        # ----------
        # ----------
        # -----X----
        # ----------
        # ----------
        # ----------

        width = 10
        height = 6

        point_mocks = [[CanvasTests.PointMock('-') for _ in xrange(height)] for _ in xrange(width)]
        point_mocks[3][3].color = 'X'

        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: point_mocks[x][y]
        canvas = Canvas(width, height, point_factory_mock)

        expected_points = {
            point_mocks[3][3],
        }
        self.assertSetEqual(expected_points, canvas.connected(3, 3))

    def test_connected_vertically_split_canvas(self):
        # -X--
        # -X--
        # -X--
        # -X--

        width = 4
        height = 4

        point_mocks = [[CanvasTests.PointMock('-') for _ in xrange(height)] for _ in xrange(width)]
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
        self.assertSetEqual(expected_points, canvas.connected(0, 0))

    def test_connected_horizontally_split_canvas(self):
        # ----
        # XXXX
        # ----
        # ----

        width = 4
        height = 4

        point_mocks = [[CanvasTests.PointMock('-') for _ in xrange(height)] for _ in xrange(width)]
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
        self.assertSetEqual(expected_points, canvas.connected(0, 0))

    def test_connected_happy_test(self):
        # --------X-
        # --------X-
        # -----X----
        # ---XXX----
        # ----XXXX--
        # ----------

        width = 10
        height = 6

        point_mocks = [[CanvasTests.PointMock('-') for _ in xrange(height)] for _ in xrange(width)]
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
        self.assertSetEqual(expected_points, canvas.connected(3, 3))


class PointTests(unittest.TestCase):
    def test_constructor(self):
        p = Point(3, 4, 'O', {'O', 'X'})
        self.assertEqual(3, p.x)
        self.assertEqual(4, p.y)
        self.assertEqual('O', p.color)

    def test_color_set_with_valid_color(self):
        p = Point(3, 4, 'O', {'O', 'X'})
        p.color = 'X'
        self.assertEqual('X', p.color)

    def test_colour_set_with_invalid_color_throws_exception(self):
        def set_color(p, color):
            p.color = color
        p = Point(3, 4, 'O', {'O', 'X'})
        self.assertRaises(ValueError, set_color, p, '#')


class PainterTests(unittest.TestCase):
    def test_draw_horizontal_line(self):
        point_mocks = [mock.Mock(), mock.Mock()]
        canvas_mock = mock.Mock()
        canvas_mock.horizontal_line = mock.Mock(return_value=point_mocks)

        painter = Painter(canvas_mock)
        painter.draw_horizontal_line(x1=2, x2=5, y=3, color='X')

        canvas_mock.horizontal_line.assert_called_once_with(x1=2, x2=5, y=3)
        for point in point_mocks:
            self.assertEqual('X', point.color)

    def test_draw_vertical_line(self):
        point_mocks = [mock.Mock(), mock.Mock()]
        canvas_mock = mock.Mock()
        canvas_mock.vertical_line = mock.Mock(return_value=point_mocks)

        painter = Painter(canvas_mock)
        painter.draw_vertical_line(x=2, y1=2, y2=5, color='X')

        canvas_mock.vertical_line.assert_called_once_with(x=2, y1=2, y2=5)
        for point in point_mocks:
            self.assertEqual('X', point.color)

    def test_draw_rectangle(self):
        canvas_mock = mock.Mock()

        draw_horizontal_line_mock = mock.Mock()
        draw_vertical_line_mock = mock.Mock()

        painter = Painter(canvas_mock)
        painter.draw_horizontal_line = draw_horizontal_line_mock
        painter.draw_vertical_line = draw_vertical_line_mock

        painter.draw_rectangle(x1=2, x2=5, y1=2, y2=5, color='X')

        draw_horizontal_line_mock.assert_has_calls([
            mock.call(x1=2, x2=5, y=2, color='X'),
            mock.call(x1=2, x2=5, y=5, color='X'),
        ])
        draw_vertical_line_mock.assert_has_calls([
            mock.call(x=2, y1=2, y2=5, color='X'),
            mock.call(x=5, y1=2, y2=5, color='X'),
        ])

    def test_bucket_fill(self):
        point_mocks = {mock.Mock(), mock.Mock()}
        canvas_mock = mock.Mock()
        canvas_mock.connected = mock.Mock(return_value=point_mocks)

        painter = Painter(canvas_mock)
        painter.bucket_fill(123, 324, 'X')

        for point in point_mocks:
            self.assertEqual('X', point.color)


if __name__ == "__main__":
    unittest.main()

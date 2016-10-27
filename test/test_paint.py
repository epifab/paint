from paint import *
import unittest
import mock


class CanvasTests(unittest.TestCase):
    def test_constructor_with_non_positive_x_throws_exception(self):
        self.assertRaises(AssertionError, Canvas, -1, 2, mock.Mock())
        self.assertRaises(AssertionError, Canvas, 0, 2, mock.Mock())

    def test_constructor_with_non_positive_y_throws_exception(self):
        self.assertRaises(AssertionError, Canvas, 1, -1, mock.Mock())
        self.assertRaises(AssertionError, Canvas, 1, 0, mock.Mock())

    def test_get_point_in_range(self):
        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: (x, y)
        canvas = Canvas(10, 8, point_factory_mock)
        self.assertEquals((3, 4), canvas.point(3, 4))
        self.assertEquals((0, 0), canvas.point(0, 0))
        self.assertEquals((0, 7), canvas.point(0, 7))
        self.assertEquals((9, 0), canvas.point(9, 0))
        self.assertEquals((9, 7), canvas.point(9, 7))

    def test_get_point_out_of_range(self):
        point_factory_mock = mock.Mock()
        point_factory_mock.create_point = lambda x, y: (x, y)
        canvas = Canvas(10, 8, point_factory_mock)
        self.assertRaises(PointOutOfCanvas, canvas.point, 13, 12)
        self.assertRaises(PointOutOfCanvas, canvas.point, 10, 0)
        self.assertRaises(PointOutOfCanvas, canvas.point, 0, 8)


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


if __name__ == "__main__":
    unittest.main()

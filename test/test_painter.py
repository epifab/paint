from paint import *
import unittest
from unittest import mock


class PainterTests(unittest.TestCase):
    def test_draw_line(self):
        expected_canvas = [
            "      ",
            "  XXX ",
            "      ",
        ]

        def line_mock(x1, y1, x2, y2):
            if (x1, y1) == (2, 1) and (x2, y2) == (4, 1):
                return [
                    Point(2, 1, ' '), Point(3, 1, ' '), Point(4, 1, ' ')
                ]
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

        def rectangle_mock(x1, y1, x2, y2):
            if (x1, y1) == (2, 0) and (x2, y2) == (4, 2):
                return {
                    Point(2, 0, ' '), Point(3, 0, ' '), Point(4, 0, ' '),
                    Point(4, 1, ' '), Point(4, 2, ' '), Point(3, 2, ' '),
                    Point(2, 2, ' '), Point(2, 1, ' ')
                }
            else:
                raise Exception("Painter shouldn't need to get any other rectangle")

        canvas_mock = mock.Mock()
        canvas_mock.width = 6
        canvas_mock.height = 3
        canvas_mock.point = lambda x, y: Point(x, y, ' ')
        canvas_mock.rectangle = rectangle_mock

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
                    Point(2, 0, ' '), Point(3, 0, ' '), Point(4, 0, ' '),
                    Point(2, 1, ' '), Point(3, 1, ' '), Point(4, 1, ' '),
                    Point(2, 2, ' '), Point(3, 2, ' '), Point(4, 2, ' '),
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

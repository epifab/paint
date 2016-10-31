import unittest
from paint import *


class ProgramTests(unittest.TestCase):
    def _assert_canvas_equals(self, canvas, expeted_visual_canvas):
        for y in xrange(len(expeted_visual_canvas)):
            for x in xrange(len(expeted_visual_canvas[y])):
                self.assertEquals(expeted_visual_canvas[y][x], canvas.point(x, y).color)

    class CanvasPrinterStub(AsciiCanvasPrinter):
        def __init__(self):
            self.printed_canvas = ""

        def print_canvas(self, canvas):
            self.printed_canvas = self.canvas_to_str(canvas)

    def test_run(self):
        printer_mock = ProgramTests.CanvasPrinterStub()
        program = Program(printer=printer_mock, palette={' ', 'x', 'o'}, foreground_color='x', background_color=' ')

        expected_canvas1 = \
            "----------------------\n" \
            "|                    |\n" \
            "|                    |\n" \
            "|                    |\n" \
            "|                    |\n" \
            "----------------------"
        expected_canvas2 = \
            "----------------------\n" \
            "|                    |\n" \
            "|xxxxxx              |\n" \
            "|                    |\n" \
            "|                    |\n" \
            "----------------------"
        expected_canvas3 = \
            "----------------------\n" \
            "|                    |\n" \
            "|xxxxxx              |\n" \
            "|     x              |\n" \
            "|     x              |\n" \
            "----------------------"
        expected_canvas4 = \
            "----------------------\n" \
            "|               xxxxx|\n" \
            "|xxxxxx         x   x|\n" \
            "|     x         xxxxx|\n" \
            "|     x              |\n" \
            "----------------------"
        expected_canvas5 = \
            "----------------------\n" \
            "|oooooooooooooooxxxxx|\n" \
            "|xxxxxxooooooooox   x|\n" \
            "|     xoooooooooxxxxx|\n" \
            "|     xoooooooooooooo|\n" \
            "----------------------"

        program.run_command("C", 20, 4)
        self.assertEquals(printer_mock.printed_canvas, expected_canvas1)

        program.run_command("L", 1, 2, 6, 2)
        self.assertEquals(printer_mock.printed_canvas, expected_canvas2)

        program.run_command("L", 6, 3, 6, 4)
        self.assertEquals(printer_mock.printed_canvas, expected_canvas3)

        program.run_command("R", 16, 1, 20, 3)
        self.assertEquals(printer_mock.printed_canvas, expected_canvas4)

        program.run_command("B", 10, 3, "o")
        self.assertEquals(printer_mock.printed_canvas, expected_canvas5)

        program.run_command("Z")
        self.assertEquals(printer_mock.printed_canvas, expected_canvas4)

        program.run_command("Z")
        self.assertEquals(printer_mock.printed_canvas, expected_canvas3)

        program.run_command("Y")
        self.assertEquals(printer_mock.printed_canvas, expected_canvas4)

        program.run_command("Y")
        self.assertEquals(printer_mock.printed_canvas, expected_canvas5)

        self.assertRaises(Quit, program.run_command, "Q")


if __name__ == "__main__":
    unittest.main()

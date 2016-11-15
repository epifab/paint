from paint import *
import unittest


class ProgramTests(unittest.TestCase):
    def _assert_canvas_equals(self, canvas, expeted_visual_canvas):
        for y in range(len(expeted_visual_canvas)):
            for x in range(len(expeted_visual_canvas[y])):
                self.assertEqual(expeted_visual_canvas[y][x], canvas.point(x, y).color)

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
            "|          x    xxxxx|\n" \
            "|xxxxxx   x x   x   x|\n" \
            "|     x  x   x  xxxxx|\n" \
            "|     x xxxxxxx      |\n" \
            "----------------------"
        expected_canvas6 = \
            "----------------------\n" \
            "|          x    xxxxx|\n" \
            "|xxxxxx   xox   x   x|\n" \
            "|     x  xooox  xxxxx|\n" \
            "|     x xxxxxxx      |\n" \
            "----------------------"

        program.run_command("C", 20, 4)
        self.assertEqual(printer_mock.printed_canvas, expected_canvas1)

        program.run_command("L", 1, 2, 6, 2)
        self.assertEqual(printer_mock.printed_canvas, expected_canvas2)

        program.run_command("L", 6, 3, 6, 4)
        self.assertEqual(printer_mock.printed_canvas, expected_canvas3)

        program.run_command("R", 16, 1, 20, 3)
        self.assertEqual(printer_mock.printed_canvas, expected_canvas4)

        program.run_command("T", 11, 1, 8, 4, 14, 4)
        self.assertEqual(printer_mock.printed_canvas, expected_canvas5)

        program.run_command("B", 10, 3, "o")
        self.assertEqual(printer_mock.printed_canvas, expected_canvas6)

        program.run_command("Z")
        self.assertEqual(printer_mock.printed_canvas, expected_canvas5)

        program.run_command("Z")
        self.assertEqual(printer_mock.printed_canvas, expected_canvas4)

        program.run_command("Z")
        self.assertEqual(printer_mock.printed_canvas, expected_canvas3)

        program.run_command("Z")
        self.assertEqual(printer_mock.printed_canvas, expected_canvas2)

        program.run_command("Y")
        self.assertEqual(printer_mock.printed_canvas, expected_canvas3)

        program.run_command("R", 16, 1, 20, 3)
        self.assertEqual(printer_mock.printed_canvas, expected_canvas4)

        # The previous action destroyed the future history
        program.run_command("Y")
        self.assertEqual(printer_mock.printed_canvas, expected_canvas4)

        self.assertRaises(Quit, program.run_command, "Q")


if __name__ == "__main__":
    unittest.main()

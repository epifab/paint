from paint import *


class CommandError(Exception):
    pass


class Quit(Exception):
    pass


class AsciiCanvasPrinter(object):
    def print_canvas(self, canvas):
        print(self.canvas_to_str(canvas))

    def canvas_to_str(self, canvas):
        canvas_str = ("-" * (canvas.width + 2)) + "\n"
        canvas_str += ("\n".join("|" + line + "|" for line in self.canvas_to_list(canvas))) + "\n"
        canvas_str += ("-" * (canvas.width + 2))
        return canvas_str

    def canvas_to_list(self, canvas):
        return [
            "".join(
                canvas.point(x, y).color
                for x in xrange(canvas.width)
            )
            for y in xrange(canvas.height)
        ]


class Program(object):
    def __init__(self, printer, palette, background_color, foreground_color):
        self._printer = printer
        self._palette = palette
        self._background_color = background_color
        self._foreground_color = foreground_color
        self._canvas = None
        self._commands = {
            'Q': self.quit_command,
            'C': self.canvas_command,
            'L': self.draw_line_command,
            'R': self.draw_rectangle_command,
            'B': self.bucket_fill_command
        }

    @property
    def canvas(self):
        return self._canvas

    def quit_command(self, args):
        raise Quit

    def canvas_command(self, args):
        try:
            width = int(args[0])
            assert width > 0
        except (IndexError, ValueError, AssertionError):
            raise CommandError("Invalid canvas width")

        try:
            height = int(args[1])
            assert height > 0
        except (ValueError, IndexError, AssertionError):
            raise CommandError("Invalid canvas height")

        self._canvas = Canvas(width, height, PointFactory(self._background_color, self._palette))

    def draw_line_command(self, args):
        x1 = self._get_x_parameter(args, 0)
        y1 = self._get_y_parameter(args, 1)
        x2 = self._get_x_parameter(args, 2)
        y2 = self._get_y_parameter(args, 3)

        if x1 == x2:
            Painter(self._canvas).draw_vertical_line(x1, y1, y2, self._foreground_color)
        elif y1 == y2:
            Painter(self._canvas).draw_horizontal_line(x1, x2, y1, self._foreground_color)
        else:
            raise CommandError("Diagonal lines are not supported yet")

    def draw_rectangle_command(self, args):
        x1 = self._get_x_parameter(args, 0)
        y1 = self._get_y_parameter(args, 1)
        x2 = self._get_x_parameter(args, 2)
        y2 = self._get_y_parameter(args, 3)

        Painter(self._canvas).draw_rectangle(x1, y1, x2, y2, self._foreground_color)

    def bucket_fill_command(self, args):
        x = self._get_x_parameter(args, 0)
        y = self._get_y_parameter(args, 1)
        color = self._get_color_parameter(args, 2)
        Painter(self._canvas).bucket_fill(x, y, color)

    def _get_x_parameter(self, params, position):
        if self._canvas is None:
            raise CommandError("Canvas not initialized")
        try:
            x = int(params[position])
            x -= 1  # points coordinate are assumed to be 1-based
            assert (x >= 0)
            assert (x < self._canvas.width)
        except IndexError:
            raise CommandError("Missing parameter {}".format(position))
        except ValueError:
            raise CommandError("Invalid parameter {}: not a number".format(position))
        except AssertionError:
            raise CommandError("Invalid parameter {}: x out of range".format(position))
        else:
            return x

    def _get_y_parameter(self, params, position):
        if self._canvas is None:
            raise CommandError("Canvas not initialized")
        try:
            y = int(params[position])
            y -= 1  # points coordinate are assumed to be 1-based
            assert (y >= 0)
            assert (y < self._canvas.height)
        except IndexError:
            raise CommandError("Missing parameter {}".format(position))
        except ValueError:
            raise CommandError("Invalid parameter {}: not a number".format(position))
        except AssertionError:
            raise CommandError("Invalid parameter {}: y out of range".format(position))
        else:
            return y

    def _get_color_parameter(self, params, position):
        try:
            c = params[position]
            assert c in self._palette
        except IndexError:
            raise CommandError("Missing parameter {}".format(position))
        except AssertionError:
            raise CommandError("Invalid parameter {}: invalid color".format(position))
        else:
            return c

    def run_command(self, command_name, *args):
        if command_name not in self._commands:
            raise CommandError("Unknown command")
        self._commands[command_name](args)
        self._printer.print_canvas(self._canvas)

    def run(self):
        while True:
            try:
                command_args = raw_input("enter command: ").split(" ")
                self.run_command(*command_args)
            except Quit:
                break
            except CommandError as e:
                print(e.args[0])

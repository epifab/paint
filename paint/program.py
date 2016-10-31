from paint import *
import copy


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
                for x in range(canvas.width)
            )
            for y in range(canvas.height)
        ]


class ProgramState(object):
    def __init__(self, palette, background_color, foreground_color):
        self.palette = palette
        self.background_color = background_color
        self.foreground_color = foreground_color
        self.canvas = None
        self.undo = []
        self.redo = []


class CommandParameters(object):
    def __init__(self, params):
        self.params = params

    def get_parameter(self, position, name, validate=lambda x: True, convert=str):
        try:
            value = convert(self.params[position])
            if not validate(value):
                raise CommandError("Invalid parameter {}".format(name))
            return value
        except ValueError:
            raise CommandError("Invalid parameter {}".format(name))
        except IndexError:
            raise CommandError("Parameter {} is missing".format(name))


class Command(object):
    def __init__(self, state, parameters):
        self.state = state
        self.parameters = parameters

    def execute(self):
        raise NotImplemented


class QuitCommand(Command):
    def execute(self):
        raise Quit


class CanvasCommand(Command):
    def execute(self):
        width = self.parameters.get_parameter(1, "width", convert=int, validate=lambda x: x > 0)
        height = self.parameters.get_parameter(2, "height", convert=int, validate=lambda x: x > 0)

        old_canvas = self.state.canvas
        new_canvas = Canvas(width, height, PointFactory(self.state.background_color))

        def undo():
            self.state.canvas = old_canvas
            self.state.redo.append(do)

        def do():
            self.state.canvas = new_canvas
            self.state.undo.append(undo)

        do()
        self.state.redo = []


class PainterCommand(Command):
    def paint(self, canvas):
        raise NotImplemented

    def get_x_parameter(self, position, name):
        return self.parameters.get_parameter(
            position,
            name,
            convert=int,
            validate=lambda x: 1 <= x <= self.state.canvas.width
        ) - 1  # User input is 1-based

    def get_y_parameter(self, position, name):
        return self.parameters.get_parameter(
            position,
            name,
            convert=int,
            validate=lambda y: 1 <= y <= self.state.canvas.height
        ) - 1  # User input is 1-based

    def execute(self):
        if not self.state.canvas:
            raise CommandError("Please create a canvas first")

        old_canvas = self.state.canvas
        new_canvas = copy.deepcopy(self.state.canvas)

        self.paint(new_canvas)

        def undo():
            self.state.canvas = old_canvas
            self.state.redo.append(do)

        def do():
            self.state.canvas = new_canvas
            self.state.undo.append(undo)

        do()
        self.state.redo = []


class LineCommand(PainterCommand):
    def paint(self, canvas):
        x1 = self.get_x_parameter(1, "x1")
        y1 = self.get_y_parameter(2, "y1")
        x2 = self.get_x_parameter(3, "x2")
        y2 = self.get_y_parameter(4, "y2")
        Painter(canvas).draw_line(x1=x1, y1=y1, x2=x2, y2=y2, color=self.state.foreground_color)


class BucketFillCommand(PainterCommand):
    def paint(self, canvas):
        x = self.get_x_parameter(1, "x")
        y = self.get_y_parameter(2, "y")
        color = self.parameters.get_parameter(3, "color", convert=str, validate=lambda c: c in self.state.palette)
        Painter(canvas).bucket_fill(x=x, y=y, color=color)


class RectangleCommand(PainterCommand):
    def paint(self, canvas):
        x1 = self.get_x_parameter(1, "x1")
        y1 = self.get_y_parameter(2, "y1")
        x2 = self.get_x_parameter(3, "x2")
        y2 = self.get_y_parameter(4, "y2")
        Painter(canvas).draw_rectangle(x1=x1, y1=y1, x2=x2, y2=y2, color=self.state.foreground_color)


class UndoCommand(Command):
    def execute(self):
        try:
            undo = self.state.undo.pop()
        except IndexError:
            pass
        else:
            undo()


class RedoCommand(Command):
    def execute(self):
        try:
            redo = self.state.redo.pop()
        except IndexError:
            pass
        else:
            redo()


class Program(object):
    def __init__(self, printer, palette, background_color, foreground_color):
        self.printer = printer
        self.state = ProgramState(palette, background_color, foreground_color)
        self.commands = {
            'Q': QuitCommand,
            'C': CanvasCommand,
            'L': LineCommand,
            'R': RectangleCommand,
            'B': BucketFillCommand,
            'Z': UndoCommand,
            'Y': RedoCommand,
        }

    def run_command(self, *args):
        parameters = CommandParameters(args)
        command_name = parameters.get_parameter(0, "command name", convert=lambda x: str(x).upper())
        if command_name not in self.commands:
            raise CommandError("Unknown command")
        command = self.commands[command_name](self.state, parameters)
        command.execute()
        if self.state.canvas:
            self.printer.print_canvas(self.state.canvas)

    def run(self):
        while True:
            try:
                command_args = raw_input("enter command: ").split(" ")
                self.run_command(*command_args)
            except Quit:
                break
            except CommandError as e:
                print(e.args[0])

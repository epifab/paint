from paint import Program, AsciiCanvasPrinter
import string

if __name__ == "__main__":
    Program(
        printer=AsciiCanvasPrinter(),
        palette={c for c in " " + string.ascii_lowercase},
        background_color=" ",
        foreground_color="x"
    ).run()

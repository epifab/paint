from .canvas import EditedCanvas


class Painter(object):
    def __init__(self, point_factory):
        self._point_factory = point_factory

    def draw_line(self, canvas, x1, y1, x2, y2, color):
        """
        Paints the line between (x1, y1) and (x2, y2)
        """
        return EditedCanvas(
            canvas=canvas,
            delta={
                (x, y): self._point_factory.create_point(x, y, color)
                for x, y in canvas.line(x1=x1, y1=y1, x2=x2, y2=y2)
            }
        )

    def draw_rectangle(self, canvas, x1, y1, x2, y2, color):
        """
        Paints the border of the rectangle with corners in (x1, y1) and (x2, y2)
        """
        return EditedCanvas(
            canvas=canvas,
            delta={
                (x, y): self._point_factory.create_point(x, y, color)
                for x, y in canvas.rectangle(x1, y1, x2, y2)
            }
        )

    def draw_polygon(self, canvas, color, *args):
        """
        Draws a polygon
        """
        return EditedCanvas(
            canvas=canvas,
            delta={
                (x, y): self._point_factory.create_point(x, y, color)
                for x, y in canvas.polygon(*args)
            }
        )

    def bucket_fill(self, canvas, x, y, color):
        """
        Paints the area connected to (x, y)
        """
        return EditedCanvas(
            canvas=canvas,
            delta={
                (x, y): self._point_factory.create_point(x, y, color)
                for x, y in canvas.uniform_area(x, y)
            }
        )

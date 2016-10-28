
Install:
1) install python 2.7 and pip
2) pip install -r requirements.txt

Run:
python run.py

Test:
python -m unittest discover


The domain objects (Canvas, Point and Painter) can be found in paint.py.
In order to decouple Canvas and Point creation, I also implemented a PointFactory which needs to be injected in the
Canvas constructor and it's used by the Canvas to create the point matrix.

Program is responsible for parsing, validating and running commands (in a REPL fashion).
To respect the single responsibility principle, a "printer" class has to be injected into the Program constructor.

Happy painting!

import pathlib
import inspect


class Path(type(pathlib.Path())):
    @staticmethod
    def script_dir():
        print(inspect.stack()[1].filename)
        p = pathlib.Path(inspect.stack()[1].filename)
        return p.parent.resolve()
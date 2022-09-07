""" redefine the Path library class """

import pathlib
import inspect


class Path(type(pathlib.Path())):
    """ new Path class declaration """

    @staticmethod
    def script_dir():
        """ get the current script path """
        #print(inspect.stack()[1].filename)
        _current_script = pathlib.Path(inspect.stack()[1].filename)
        return _current_script.parent.resolve()

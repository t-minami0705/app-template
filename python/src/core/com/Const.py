# -*- coding: utf-8 -*-
class _Const:
    """ Constant generation class.
    :author: T.Minami
    :version: 1.0.0
    :since: 1.0.0
    :note:
        Since Python does not have built-in constant support, this class prevents 
        the duplicate definition of constants.
        Attempting to overwrite a value once it has been set will raise an error.
        When this module is imported, the module itself is replaced with an instance of this class.	
    """
    class _ConstTypeError(TypeError):
        """ Exception raised when a constant is defined more than once. """
        pass
    
    def __repr__(self) -> str:
        """ Return a string representation of this instance. """
        return "Constant type definitions."
    
    def __setattr__(self, name: str, value: object) -> None:
        """Set a constant value.

        :param name: Constant name.
        :param value: Constant value.
        :raises _ConstTypeError: If the constant is already defined with a different value.
        """
        result = self.__dict__.get(name, value)
        if result != value:
            msgstr = f"Duplicate constant definition. Before:{result} , After:{value}"
            raise self._ConstTypeError(msgstr)
        self.__dict__[name] = value
        
    def __del__(self) -> None:
        """Clear all constants when the instance is deleted."""
        self.__dict__.clear()


import sys
# Replace this module with an instance of _Const.
# This allows constants to be defined directly as module attributes.
# e.g.) import Const
#     Const.MAX_COUNT = 100
sys.modules[__name__] = _Const()

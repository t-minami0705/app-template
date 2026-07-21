# -*- coding: utf-8 -*-
class BaseResult:
    """ Base result class for all common classes.
    :author: T.Minami
    :version: 1.0.0
    :since: 1.0.0
    :note:
        Base class to be inherited by all common classes.
        Stores the execution result and allows the caller
        to determine success or failure.
    """
    def __init__(self):
        self._class_name: str = ""
        self._method_name: str = ""
        self._result_code: int = 0
        self._result_mag: str = ""
        self._result_errmsg: str = ""
        self._stack_trace: str = ""

    # ========================================================================================
    # Properties
    # ========================================================================================
    @property
    def class_name(self) -> str:
        return self._class_name 
    
    @class_name.setter
    def class_name(self, value: str) -> None:
        self._class_name = value

    @property
    def method_name(self) -> str:
        return self._method_name
    
    @method_name.setter
    def method_name(self, value: str) -> None:
        self._method_name = value
    
    @property
    def result_code(self) -> int:
        return self._result_code
    
    @result_code.setter
    def result_code(self, value: int) -> None:
        self._result_code = value
    
    @property
    def result_msg(self) -> str:
        return self._result_mag

    @result_msg.setter
    def result_msg(self, value: str) -> None:
        self._result_mag = value
    
    @property
    def result_errmsg(self) -> str:
        return self._result_errmsg
    
    @result_errmsg.setter
    def result_errmsg(self, value: str) -> None:
        self._result_errmsg = value

    @property
    def stack_trace(self) -> str:
        return self._stack_trace

    @stack_trace.setter
    def stack_trace(self, value: str) -> None:
        self._stack_trace = value

    # ========================================================================================
    # Private Methods
    # ========================================================================================
    def _initalize(self) -> None:
        """ Initialize the result values.
        """
        self._method_name = ""
        self._result_code = 0
        self._result_mag = ""
        self._result_errmsg = ""
        self._stack_trace = ""
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
        self.className: str = ""
        self.methodName: str = ""
        self.resultCode: int = 0
        self.resultMsg: str = ""
        self.resultErrMsg: str = ""
        self.stackTrace: str = ""


from thonnycontrib.properties import CANNOT_RUN_TESTS_MSG
import inspect, thonnycontrib.exceptions as exceptions

class ExceptionResponse:
    """
    Cette classe est utilisée pour encapsuler les exceptions levées par le plugin l1test.
    Il prend en argument une exception levée et représente cette exception sous forme d'un 
    message qui sera affiché à l'utilisateur.
    
    Note: use the `str()` method to get the message like str(ExceptionResponse(e)).
    
    Example:
    >>> try:
    ...     1/0
    ... except Exception as e:
    ...     print(ExceptionResponse(e))
    ...
    ZeroDivisionError:
    division by zero
    """
    def __init__(self, exception:BaseException) -> None:
        self.__exception = exception
        self.__type_name = exception.__class__.__name__
        self.__message = str(exception) # cannot be accessed directly, use __str__ instead
        self.__title = CANNOT_RUN_TESTS_MSG
    
    # getters/setters
    def get_exception(self):
        return self.__exception
    
    def get_type_name(self) -> str:
        return self.__type_name
            
    def get_title(self) -> str:
        return self.__title
    
    def set_exception(self, exception:BaseException):
        self.__exception = exception
        
    def set_title(self, title:str):
        self.__title = (title if title else CANNOT_RUN_TESTS_MSG)
    
    def __str__(self) -> str:        
        super_cls = inspect.getmro(self.__exception.__class__) # get the super classes of the exception
        for l1test_exception in [exceptions.BackendException, exceptions.FrontendException]:                
            if (l1test_exception in super_cls):
                return self.__message
        
        # si on est là alors l'exception levée n'est pas une exception l1test est
        # c'est probablement une exception levée par python.
        return "%s:\n%s" % (self.__type_name, self.__message)
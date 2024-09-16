# Module Evaluator

from thonnycontrib.backend.models import L1TestModule
from .ast_parser import L1TestAstParser
from thonnycontrib.exceptions import *
from thonnycontrib.utils import *
from .doctest_parser import *
from thonny import *
from types import ModuleType
from ..i18n.languages import tr

@tostring
class Evaluator:
    """
    The Evaluator, in short, allows to evaluate all the tests retrieved in the given source
    and returns the verdicts. 
    
    Actually, it invokes the L1TestAstParser to parse and retrieve the tests (called L1Doctests) 
    from the source. Then, to evaluate the L1Doctests it needs the context about the declared 
    functions in the source, for that it imports the module from the given filename. 
    
    Finally, after the evaluation is finished, the verdicts are returned as a list of 
    the evaluated `L1Doctest` wrapped in L1TestModule instance. For more details see the documentation of L1DocTest and L1TestModule.
        
    Args:
        - filename (str, optional): the filename to be executed by the `Evaluator`. Defaults to "".
        - l1test_ast_parser (L1TestAstParser, optional): the parser to be used to parse the source. Defaults to None.
        - filter_predicate (Callable[[L1DocTest], bool], optional): the predicate to be used to filter the L1Doctests. 
            It's a function that takes a L1doctest as argument and returns True if the node is accepted, otherwise 
            it returns False. Defaults to None (ie. means that no filtering will be applied).
        - should_notify_listeners (bool, optional): if True, the listeners will be notified about the state of the execution. 
            Defaults to True.
    """
    def __init__(self, filename:str="", l1test_ast_parser: L1TestAstParser=None):
        self._module: ModuleType = None
        self._l1test_ast_parser = l1test_ast_parser if l1test_ast_parser else L1TestAstParser(filename=filename)
        self._l1test_ast_parser.set_filename(filename)
            
    def evaluate(self, source:str) -> L1TestModule:
        """
        Imports the module from the filename, sets the global variables to
        imported module's dict and then evaluates the tests.
        
        Args:
            source (str): the source code to be parsed by the `TestFinder`.
        
        Returns:
            L1ModuleTest: Returns the module containing the evaluated tests.
        """
        # si le `self._module` est null, alors `Evaluator` va s'occuper d'importer lui même
        # le module à partir du filename. 
        # Sinon, le module a été fournit, donc `Evaluator` utilisera le module fournit.
        if not self._module:
            # The `import_module()` function can raise an exception(see it's doc)
            self.set_module(self._import_module(self.get_filename()))
        
        return self.__parse_and_evaluate(source) 
    
    def __parse_and_evaluate(self, source:str) -> L1TestModule:
        """
        Parse the source and evaluates the extracted tests.
        
        Args:
            source (str): the source code to be parsed by the `TestFinder`.
        
        Returns:
            List[L1DocTest]: Returns the module containing the evaluated tests.
        
        Raises:
            Error: A compilation error raised by the AST module.
            SpaceMissingAfterPromptException: when a space is missing after the prompt.
        """
        # This line parses the source using the AST module and can raise a compilation error 
        l1ModuleTest = self._l1test_ast_parser.parse(source) 
        l1ModuleTest.evaluate(self._module.__dict__.copy())    
        return l1ModuleTest     
    
    def _import_module(self, filename:str) -> ModuleType:
        """
        Import a module from a given filename. 
        The ~filename~ can be also the absolute path of a file.
        
        This function can raise an exception if the imported module 
        contains a compilation error. You should catch it somewhere.
        
        Args:
            filename (str): The filename(or the absolute path) of a file

        Returns:
            ModuleType: Returns the corresponding module of the given file.
            
        Raises: 
            CannotImportModuleException: if the filename cannot be imported by the 
            importlib module.
            CompilationError: any other exception related to a compilation error.
        """
        import importlib.util as iu, os, sys
        
        # import the module specification. 
        # To learn more about ModuleSpec `https://peps.python.org/pep-0451/`    
        module_name = get_module_name(filename)
        spec = iu.spec_from_file_location(module_name, filename)
        if not spec: 
            if not filename.endswith(".py"):
                msg_error = tr("The file \"%s\" cannot be imported.\n\n" + 
                            "Please, be sure that the extension of the file is `.py`") % filename 
            else:
                msg_error = tr("Cannot found the file `%s`") % filename 
            msg_error = tr("Error when importing the module \"%s\":\n%s") % (module_name, msg_error)
            raise CannotImportModuleException(msg_error)
        
        imported_source = iu.module_from_spec(spec)
        
        workingdir = os.path.split(imported_source.__file__)
        if (len(workingdir) > 0):
            basedir = workingdir[0]
            dirs = self.__get_all_parent_directories(basedir)
            
            # ajout des packages parents au sys.path
            # on fait ça parce que on veut assurer les imports 
            # des fichiers contenant dans les packages parents
            [sys.path.append(path) for path in dirs]
            
            # ajout des sous packages au sys.path 
            # pour assurer les imports des fichiers contenant dans les sous packages
            sub_packages = self.__get_sub_directories(basedir)
            [sys.path.append(basedir + os.sep + path) for path in sub_packages]
    
        try:
            # This line can raise an exception if the module contains compilation errors,
            # or if the module imports non existed modules
            spec.loader.exec_module(imported_source) 
            return imported_source
        except BaseException as e:
            # the compilation error is catched and raised as a CompilationError
            # and the evaluation is interrupted(because we cannot parse a content
            # with compilation errors).
            error_info = sys.exc_info()
            formatted_error = get_last_exception(error_info)
            raise CompilationError(formatted_error) 
    
    def __get_all_parent_directories(self, dir_path:str):
        """
        For a given path of a directory returns all the parents directory from that path.
        
        Examples:
        >>> get_all_parent_directories('/home/stuff/src')
        ['/home', '/home/stuff', '/home/stuff/src']
        """
        import os
        
        if dir_path is None:
            return []
        
        dirs = dir_path.split(os.sep)
        m = ""
        res = []
        for e in dirs[1:]:
            m += os.sep + e  
            res.append(m)
        return res

    def __get_sub_directories(self, package_path:str):
        """
        Get all sub-packages of a given package(param). 
        """
        from setuptools import find_packages
        return [p.replace(".", os.sep) for p in find_packages(package_path)]

    def get_module(self):
        return self._module

    def set_module(self, module: ModuleType):
        self._module = module
        
    def set_l1test_ast_parser(self, l1test_ast_parser: L1TestAstParser):
        self._l1test_ast_parser = l1test_ast_parser
    
    def get_l1test_ast_parser(self):
        return self._l1test_ast_parser

    def set_filename(self, filename:str):
        self._l1test_ast_parser.set_filename(filename)
    
    def get_filename(self):
        return self._l1test_ast_parser.get_filename()
    

from abc import *
from typing import List
from thonnycontrib.backend.models import L1DocTest, L1TestModule
from ..utils import create_node_name, tostring
from .doctest_parser import DocTestParser, Example
import ast

# Only these types can have a docstring 
# according to ast's module documentation
SUPPORTED_TYPES = (ast.FunctionDef, 
                   ast.ClassDef, 
                   ast.Module)

class L1TestAstVisitor(ast.NodeVisitor):
    """
    The `L1TestAstVisitor` is responsible for visiting the AST tree and creating the L1DocTests.

    Args:
        l1ModuleTest (L1TestModule): the module containing the L1DocTests. It will be used 
        to add the created L1DocTests.
    """
    DOCTEST_PARSER = DocTestParser()
    
    def __init__(self, l1ModuleTest:L1TestModule=L1TestModule()):
        self.l1ModuleTest = l1ModuleTest
        
    def visit(self, node):
        method_name = "visit_" + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        visitor(node)

    def generic_visit(self, node):
        for child_node in ast.iter_child_nodes(node):
            self.visit(child_node)

    def visit_FunctionDef(self, node):
        self.process_supported_node(node)

    def visit_ClassDef(self, node):
        self.process_supported_node(node)

    def visit_Module(self, node):
        self.process_supported_node(node)

    def process_supported_node(self, node): 
        l1doctest = self.create_l1doctest(node)
        self.l1ModuleTest.add_l1doctest(l1doctest)
        for child_node in ast.iter_child_nodes(node):
            self.visit(child_node)

    def create_l1doctest(self, node):
        type_name = node.__class__.__name__
        l1doctest = L1DocTest(self.l1ModuleTest, create_node_name(node), type_name, node.lineno)
        
        if node.body:
            first_stmt = node.body[0]
            if isinstance(first_stmt, ast.Expr) and isinstance(first_stmt.value, ast.Str):
                l1doctest.set_start_lineno(first_stmt.lineno)
                l1doctest.set_end_lineno(first_stmt.end_lineno)

        docstring = ast.get_docstring(node, False) or ""
        parsed_doc = self.DOCTEST_PARSER.parse(docstring, name=self.l1ModuleTest.get_filename())

        l1doctest.set_examples(self.__filter_example_instances(l1doctest, parsed_doc))

        return l1doctest
    
    def __filter_example_instances(self, l1_doctest:L1DocTest, parsed_doc:list) -> List[Example]:
        """
        The filter can return an empty list if there's no example 
        in the parsed docstring. Otherwise, it will return a list of the `Example` instances 
        matching the given l1doctest.
        """
        examples = []
        for test in parsed_doc:
            if isinstance(test, Example):
                test.lineno = test.lineno + l1_doctest.get_start_lineno() - 1
                examples.append(test)
        return examples   
    
@tostring
class L1TestAstParser(): 
    """
    The L1DocTestParser is responsible for parsing the source and extracts the L1DocTests.
    The main method is `parse()` which takes the source code as argument and returns a
    L1ModuleTest instance containing all the L1DocTests found in the source. 
    
    The `L1DocTestParser` doesn't evaluate the created L1Doctests. Each created L1DocTest
    is initially unevaluated. It's the responsibility of the `Evaluator` to evaluate each 
    received L1DocTest.
    
    Example of use:
    >>> parser = L1DocTestParser("filename.py")
    >>> l1ModuleTest = parser.parse("source") 
    """
    def __init__(self, filename:str="<string>", mode="exec", ast_visitor=None) -> None:
        self._mode = mode
        self._ast_visitor = L1TestAstVisitor() if not ast_visitor else ast_visitor
        self.set_filename(filename)

    def parse(self, source:str):
        """
        Parses the source and creates all l1doctests (type of L1Doctest) wrapped in L1TestModule.
        
        Args:
            source (str): the source code to be parsed.
         
        Returns:
            a L1ModuleTest instance containing all the L1DocTests found in the source.
        
        Raises: 
            Error: A compilation error raised by the AST module.
        """
        body = ast.parse(source, self._filename, mode=self._mode).body
        l1TestModule = self._visit(body)
        l1TestModule.set_source(source)
        return l1TestModule
    
    def _visit(self, list_nodes: List[ast.AST]):
        """
        Search all the supported nodes in the AST tree. Even sub-nodes are visited.
        """
        for node in list_nodes:
            self._ast_visitor.visit(node)

        return self._ast_visitor.l1ModuleTest
        
    def get_filename(self):
        return self._filename
    
    def set_filename(self, filename: str):
        self._filename = filename
        self._ast_visitor.l1ModuleTest.set_filename(filename)
        
    def get_mode(self):
        return self._mode
    
    def set_mode(self, mode):
        self._mode = mode
        
    def get_ast_visitor(self):
        return self._ast_visitor
    
    def set_ast_visitor(self, ast_visitor):
        self._ast_visitor = ast_visitor
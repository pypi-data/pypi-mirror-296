import textwrap
from typing import List
from thonnycontrib.environement_vars import FILTER_PREDICATE_VAR
from thonnycontrib.backend.l1test_backend import ExceptionResponse
from thonnycontrib.backend.models import *
from thonnycontrib.backend.evaluator import Evaluator
from thonnycontrib.exceptions import CliException
from thonnycontrib.frontend.l1test_runner import AbstractL1TestRunner
from thonnycontrib.properties import *

from rich.theme import Theme
from rich.style import Style
from rich.console import Console

indent = lambda n: " " * n
sep = lambda length: "~"*(length)
_SEP_LEN = 50
WELCOMING_MSG = "\n> Starting the execution of %s\n"

LINENO_COLOR = "cyan"

CONSOLE_THEMES = {
    "classic": {},
    "pretty": {
        "repr.str": "white", 
        "repr.path": Style(color="magenta")
    }
}

class L1TestCliRunner(AbstractL1TestRunner):
    def __init__(self, filename="", source="", pretty_mode=True, show_state=False, evaluator:Evaluator=None):
        super().__init__()
        self._source = source
        self.__evaluator = Evaluator() if not evaluator else evaluator
        self.__evaluator.set_filename(filename)
        self.__pretty_mode: bool = pretty_mode
        self.__show_exec_state: bool = show_state
        self.__reporter = Console(theme=Theme(CONSOLE_THEMES.get("pretty" if self.is_pretty_mode() else "classic"), 
                                              inherit=False))
    
    def _run(self, **kw): 
        try :       
            output = f"{sep(_SEP_LEN)}{WELCOMING_MSG % self.get_evaluator().get_filename()}{sep(_SEP_LEN)}\n\n" 
            
            l1test_module: L1TestModule = self.__evaluator.evaluate(self._source)

            predicate = kw.get(FILTER_PREDICATE_VAR)
            self.filter_by_predicate_if_present(l1test_module, predicate)

            output += self.__format_l1doctests(l1test_module.get_l1doctests())
            output += self.__format_summarize(l1test_module)
            
            self.__reporter.print(output)
        except BaseException as e:
            exception_response = ExceptionResponse(e)
            raise CliException(exception_response.get_title() + "\n\n" + str(exception_response))
    
    def filter_by_predicate_if_present(self, l1test_module: L1TestModule, predicate: Callable[[L1DocTest], bool] | None):
        if predicate:
            filtered = l1test_module.filter_by_predicate(predicate)
            l1test_module.set_l1doctests(filtered)
            
    def handle_execution_state(self, msg: BackendEvent):
        import sys, time 
        def delete_last_line():
            """Use this function to delete the last line in the STDOUT"""
            sys.stdout.write('\x1b[1A') # cursor up one line
            sys.stdout.write('\x1b[2K') # delete last line
        if self.__show_exec_state:
            state:ExecutionStateEnum = ExecutionStateEnum(msg.get("state"))
            match state:
                case ExecutionStateEnum.PENDING:
                    self.set_is_pending(True)
                    self.__reporter.print(START_EXECUTION_STATE_MSG % msg.get("lineno"))
                    delete_last_line() # on ne veut pas garder le message de l'état PENDING, il indique juste qu'on a commencé l'évaluation d'un test
                case ExecutionStateEnum.FINISHED_TEST:
                    duration = msg.get("duration")
                    self.__reporter.print(FINISHED_EXECUTION_STATE_MSG % (msg.get("lineno"), duration))
                case ExecutionStateEnum.FINISHED_ALL: 
                    self.set_is_pending(False) 
                    self.__reporter.print("\n")
        
    def _show_error(self, exception_response: ExceptionResponse|Exception):
        self.__reporter.print("%s\n%s" % (exception_response.get_title(), str(exception_response)))

    def __format_l1doctests(self, l1doctests: List[L1DocTest]):
        format = lambda s, c: "[%s]%s[/%s]" %(c, s, c) if self.is_pretty_mode() else s
        
        output = ""
        for i in range(len(l1doctests)):
            l1doctest = l1doctests[i]
            level = 5
            flag: L1DocTestFlag = l1doctest.get_flag() 
            color = flag.get_color(cli_mode=True)
            new_line = "\n"*2 if i > 0 else ""
            l1doctest_name = "%s%s: %s" % (format(flag.get_cli_format(), color), 
                                           format(l1doctest.get_node_lineno(), LINENO_COLOR), 
                                           format(l1doctest.get_ui_name(inline=False), color))
            output += new_line + l1doctest_name
            
            if l1doctest.has_flag(L1DocTestFlag.EMPTY):
                output += " - " + format(NO_TEST_FOUND_MSG, color) + "\n"
            else:
                output += "\n"
                examples = l1doctest.get_test_examples()
                for i in range(len(examples)):
                    example = examples[i]
                    verdict = example.get_verdict()
                    lineno = str(verdict.get_lineno())
                    new_line = "\n" if i > 0 else ""
                    output += new_line + indent(level) + "%s: %s\n" %(format(lineno, LINENO_COLOR), format(str(verdict), verdict.get_color()))
                    if not verdict.isSuccess():
                        output += textwrap.indent(verdict.get_details(), prefix=" "*(level*2)) + "\n"
        return output

    def __format_summarize(self, l1test_module: L1TestModule):
        summarize = l1test_module.get_summarize_as_string()
        longest_line = len(summarize.splitlines()[-1])
        
        space = 2
        sep = "-"*(longest_line+space+1)
        return "\n%s\n%s\n%s" %(sep, textwrap.indent(summarize, " "*space), sep)

    def set_pretty_mode(self, pretty:bool):
        self.__pretty_mode = pretty
    
    def is_pretty_mode(self):
        return self.__pretty_mode
    
    def get_evaluator(self):
        return self.__evaluator
    
    def set_evaluator(self, evaluator):
        self.__evaluator = evaluator
        
    def set_source(self, source:str):
        self._source = source
        
    def get_source(self):
        return self._source
        
    def set_filename(self, filename:str):
        self.__evaluator.set_filename(filename)
    
    def set_show_exec_state(self, value:bool):
        self.__show_exec_state = value
    
    def get_show_exec_state(self):
        return self.__show_exec_state
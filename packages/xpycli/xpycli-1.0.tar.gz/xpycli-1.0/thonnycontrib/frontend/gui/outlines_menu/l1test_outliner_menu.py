from enum import Enum
from typing import Any, Generator, List
import re
from thonny import get_workbench
from functools import partial

from thonnycontrib.environement_vars import *
from thonnycontrib.properties import PLUGIN_NAME
import tkinter as tk
from thonnycontrib.utils import  tostring, get_photoImage
from thonnycontrib.frontend import gui 

_OUTLINER_REGEX = r"\s*(?P<type>def|class)[ ]+(?P<name>[\w]+)"

class OutlinedNodeType(Enum):
    CLASS = "class"
    FUNCTION = "def"
    
    def get_gui_repr(self):
        match self.value:
            case "class":
                return "outline_class.png" 
            case "def":
                return "outline_method.gif" 
            case _:
                raise TypeError("The given type %s is not recognized" % self.value)
    
    def get_cli_repr(self):
        match self.value:
            case "class":
                return "C" 
            case "def":
                return "M" 
            case _:
                raise TypeError("The given type %s is not recognized" % self.value)

    def from_value(value: int):
        legal_values = [t.value for t in OutlinedNodeType]
        if value not in legal_values:
            raise ValueError(f"The value must be one of the following: {legal_values}")
        elif value == OutlinedNodeType.CLASS.value:
            return OutlinedNodeType.CLASS
        else:
            return OutlinedNodeType.FUNCTION
    
@tostring
class OutlinedNode():
    """
    This class represents an outlined node. An outlined node is either a class or a function.
    """ 
    def __init__(self, type:OutlinedNodeType, name:str, lineno:int) -> None:
        self.__type = type
        self.__name = name
        self.__lineno = lineno
    
    def get_type(self):
        return self.__type  
    
    def get_name(self):
        return self.__name  
    
    def get_lineno(self):
        return self.__lineno  

@tostring
class L1TestOutliner():   
    """
    This class is responsible for parsing the source code and building the menu which contains
    the outlined nodes (classes and functions). 
    
    The parsing is done using a regular expression. 
    No AST is used, because the parsing is done on the fly, when the user clicks on the menu.
    
    The regular expression is defined in the global variable `_OUTLINER_REGEX`.
    """
    def __init__(self) -> None:
        gui._outliner = self # singleton        
        # create the menu with a postcommand which will be called every time the menu is clicked
        self.menu = tk.Menu(None, postcommand=self.update_menu, tearoff=0)
    
    @staticmethod
    def parse(source:str) -> Generator[OutlinedNode, Any, None]:
        """
        Parses a source and returns a list of the outlined nodes. 
        The outlined nodes are either a class or a function. For 
        each outlined node an object of type `OutlinedNode` is built 
        in which we store the type (class/function), the name and the lineno
        of the outlined node.
        """
        lineno = 0
        for line in source.splitlines():
            lineno += 1
            match = re.match(_OUTLINER_REGEX, line) 
            if match:
                type = OutlinedNodeType.from_value(match.group("type"))
                yield OutlinedNode(type, match.group("name"), lineno)
    
    def from_source_post_menu(self, source):
        self.clear_menu()
        for outlined in L1TestOutliner.parse(source):
            label = "%s %s" % (outlined.get_type().value, outlined.get_name())
            self.menu.add_command(label=label, 
                                  image=get_photoImage(outlined.get_type().get_gui_repr()),
                                  command=partial(run_tests_for_outlined_node, outlined.get_lineno()),
                                  activebackground="white",
                                  activeforeground="darkblue",
                                  compound=tk.LEFT)
           
    def update_menu(self):
        editor = get_workbench().get_editor_notebook().get_current_editor()
        if not editor:
            self.clear_menu()
            return
        source = editor.get_code_view().get_content()
        self.from_source_post_menu(source)
    
    def clear_menu(self):
        self.menu.delete(0, tk.END)
        
    def get_menu(self):
        return self.menu

def run_tests_for_outlined_node(lineno:int):
    """
    Cette fonction est invoquée quand un item (méthode) du menu `Run test for ...` est cliqué.
    Cette fonction permet d'envoyer au l1test_backend la commande L1test avec en argument
    is_selected=True.
    """
    from thonnycontrib.frontend import get_l1test_gui_runner
    get_l1test_gui_runner().run_test_at(lineno)
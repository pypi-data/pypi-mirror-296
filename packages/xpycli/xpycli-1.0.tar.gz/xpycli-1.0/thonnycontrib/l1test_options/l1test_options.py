from tkinter import ttk
from thonny.config_ui import ConfigurationPage

from ..properties import EXECUTION_STATE_EVENT, PLUGIN_NAME
from ..i18n.languages import tr
from thonny import ui_utils
import tkinter as tk, thonny

# Default config
DEFAULT_DOCSTRING_TEMPLATE = True # true to use the default docstring, false to use a custom one
DEFAULT_DOC_GENERATION_AFTER_RETURN = True
DEFAULT_IMPORT_MODULE_IN_SHELL = True
DEFAULT_CLOSE_FUNCTION_ROWS = False
DEFAULT_OPEN_ONLY_RED_FUNCTIONS = True
DEFAULT_HIGHLIGHT_EXCEPTIONS = False
DEFAULT_REPORT_EXCEPTION_DETAIL = True 
DEFAULT_MOVE_ERRORVIEW_TO_BOTTOM = False
DEFAULT_TEXT_WRAPPING = True
DEFUALT_EXECUTION_STATE = False

# Option names
TEMPLATE_DOCSTRING = "template_docstring"
AUTO_GENERATON_DOC = "auto_generaton_doc"
IMPORT_MODULE = "import_module"
FOLD_ALL_FUNCTIONS = "close_function_rows"
EXPAND_ONLY_RED_FUNCTIONS = "open_only_red_functions"
HIGHLIGHT_EXCEPTIONS = "highlight_exceptions"
REPORT_EXCEPTION_DETAIL = "exception_detail"
MOVE_ERRORVIEW_TO_BOTTOM = "move_errorview_to_bottom"
TEXT_WRAPPING = "text_wrapping"
EXECUTION_STATE = "execution_state"

# Dict of options name and default value
OPTIONS = {
    TEMPLATE_DOCSTRING : DEFAULT_DOCSTRING_TEMPLATE,
    AUTO_GENERATON_DOC : DEFAULT_DOC_GENERATION_AFTER_RETURN,
    IMPORT_MODULE : DEFAULT_IMPORT_MODULE_IN_SHELL,
    FOLD_ALL_FUNCTIONS: DEFAULT_CLOSE_FUNCTION_ROWS,
    EXPAND_ONLY_RED_FUNCTIONS : not DEFAULT_CLOSE_FUNCTION_ROWS,
    HIGHLIGHT_EXCEPTIONS: DEFAULT_HIGHLIGHT_EXCEPTIONS,
    REPORT_EXCEPTION_DETAIL: DEFAULT_REPORT_EXCEPTION_DETAIL,
    MOVE_ERRORVIEW_TO_BOTTOM: DEFAULT_MOVE_ERRORVIEW_TO_BOTTOM,
    TEXT_WRAPPING: DEFAULT_TEXT_WRAPPING,
    EXECUTION_STATE: DEFUALT_EXECUTION_STATE
}

def init_options():
    """
    Initialise dans le workbench les options du plugin.
    """
    for opt in OPTIONS :
        if not thonny.get_workbench().get_option(opt) :
            thonny.get_workbench().set_default("%s." % PLUGIN_NAME + opt, OPTIONS[opt])

def get_option(name: str): 
    """
    Renvoie la valeur dans le workbench de l'option passée en paramètre.

    Paramètres:
    - name : le nom de l'option, tel que définie ds globals.py 
    """
    return thonny.get_workbench().get_option("%s." % PLUGIN_NAME + name)

def set_option(name, value):
    thonny.get_workbench().set_option("%s." % PLUGIN_NAME + name, value)

class L1TestConfigurationPage(ConfigurationPage):
    def __init__(self, master):
        ConfigurationPage.__init__(self, master)
        
        template_docstring = "par défault" if get_option(TEMPLATE_DOCSTRING) else "personnalisée"
        self.add_checkbox("%s.%s" % (PLUGIN_NAME, AUTO_GENERATON_DOC), 
                          tr("Generate the docstring automatically after a line break at a function name.")
                          +"\n"+tr(f"> Docstring {template_docstring} activée."))

        self.add_checkbox("%s.%s" % (PLUGIN_NAME, IMPORT_MODULE), 
                          tr("Import the module executed in the shell."))
    
        self.add_checkbox("%s.%s" % (PLUGIN_NAME, FOLD_ALL_FUNCTIONS),
                          tr("Fold all function in %s view.") % PLUGIN_NAME,
                          callback=lambda: set_option(EXPAND_ONLY_RED_FUNCTIONS, not get_option(FOLD_ALL_FUNCTIONS)))
         
        self.add_checkbox("%s.%s" % (PLUGIN_NAME, EXPAND_ONLY_RED_FUNCTIONS),
                          tr("Expand only red functions in %s view.") % PLUGIN_NAME,
                          callback=lambda: set_option(FOLD_ALL_FUNCTIONS, not get_option(EXPAND_ONLY_RED_FUNCTIONS)))
        
        self.add_checkbox("%s.%s" % (PLUGIN_NAME, HIGHLIGHT_EXCEPTIONS), 
                          tr("Highlight failed tests (only those that throw an exception)."))
        
        self.add_checkbox("%s.%s" % (PLUGIN_NAME, MOVE_ERRORVIEW_TO_BOTTOM), 
                          tr("Place the error view at the bottom of the Thonny IDE (next to the `Shell` view).\n" + 
                             "By default, the error view is placed below the `L1Test` view. Thonny must be restarted after having modified this option."))
        
        self.add_checkbox("%s.%s" % (PLUGIN_NAME, TEXT_WRAPPING), tr("Wrap text in %s view.") % PLUGIN_NAME,
                          callback=callback_text_wrapping)
        
        self.add_checkbox("%s.%s" % (PLUGIN_NAME, EXECUTION_STATE), 
                          tr("Show the execution state of the tests in the %s view.") % PLUGIN_NAME,
                          callback=callback_execution_state)
                            

    def add_checkbox(
            self, flag_name, description, callback=None, row=None, column=0, padx=0, pady=0, columnspan=1, tooltip=None
    ):
        variable = thonny.get_workbench().get_variable(flag_name)
        checkbox = ttk.Checkbutton(self, text=description, variable=variable, command=callback)
        checkbox.grid(
            row=row, column=column, sticky=tk.W, padx=padx, pady=pady, columnspan=columnspan
        )

        if tooltip is not None:
            ui_utils.create_tooltip(checkbox, tooltip)
            
def callback_text_wrapping():
    """
    Callback function for the text wrapping option.
    """
    from thonnycontrib.frontend import get_l1test_gui_runner
    set_option(TEXT_WRAPPING, not get_option(TEXT_WRAPPING))
    get_l1test_gui_runner().get_reporter().get_treeview().enable_or_disable_text_wrapping()

def callback_execution_state():
    """
    Callback function for the execution state option.
    """
    from thonnycontrib.frontend import get_l1test_gui_runner
    if get_option(EXECUTION_STATE):
        thonny.get_workbench().bind(EXECUTION_STATE_EVENT, get_l1test_gui_runner().handle_execution_state)
    else:
        thonny.get_workbench().unbind(EXECUTION_STATE_EVENT, get_l1test_gui_runner().handle_execution_state)

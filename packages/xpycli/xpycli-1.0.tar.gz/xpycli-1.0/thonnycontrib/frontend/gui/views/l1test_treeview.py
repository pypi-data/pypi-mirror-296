from thonny import  tktextext, ui_utils
from thonny import editors
from thonny.ui_utils import scrollbar_style
from thonnycontrib.backend.l1test_backend import ExceptionResponse
from thonnycontrib.backend.verdicts.PassedVerdict import PassedVerdict
from thonnycontrib.environement_vars import *
from thonnycontrib.exceptions import BackendException
from thonnycontrib.utils import get_font_size_option, get_font_family_option
from .l1test_error_view import L1TestErrorView
from thonnycontrib.properties import *
from thonnycontrib.backend.doctest_parser import Example
from thonnycontrib.backend.models import L1DocTest, L1DocTestFlag, L1TestModule, Summarize
from thonnycontrib.backend.verdicts.ExceptionVerdict import ExceptionVerdict
from thonnycontrib.backend.verdicts.FailedVerdict import FailedVerdict
from thonnycontrib.backend.verdicts.FailedWhenExceptionExpectedVerdict import FailedWhenExceptionExpectedVerdict
from thonnycontrib.utils import *
from functools import cache, partial
from thonnycontrib.l1test_options.l1test_options import *
from thonny.codeview import *
from typing import List, Tuple
from tkinter import ttk
import tkinter as tk, tkinter.font as tk_font, thonny

# La hauteur, par défault, d'une ligne dans une Treeview
ROW_HEIGHT = 40

SMALL_MARGIN = 1.1
NORMAL_MARGIN = 1.17

CLICKABLE_TAG = "clickable"

# La couleur de fond de l'en-tête de la treeview sur Windows
BACKGROUND_COLOR_WIN = "#F2F1EF"
BACKGROUND_COLOR_WIN_NAME = "BACKGROUND_COLOR_WIN"

# Palette de couleurs utilisée par la treeview
COLORS:dict = { 'orange': '#e8770e',
                'red': 'red',
                'lightred': '#ffdddb',
                'darkred': '#f7140c',
                'green': 'darkgreen',
                'blue': '#0000cc',
                'gray': 'gray',
                BACKGROUND_COLOR_WIN_NAME: BACKGROUND_COLOR_WIN
            }

RED_VERDICTS = (FailedVerdict, FailedWhenExceptionExpectedVerdict, ExceptionVerdict)    



@tostring
class L1TestTreeView(ttk.Frame):    
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master, borderwidth=0, relief="flat")
        self.workbench = thonny.get_workbench()
        self._l1test_module: L1TestModule = L1TestModule() # créez un objet L1TestModule vide
        
        self.__init_treeview()
        self.__init_special_attributes()
        
        self.__header = L1TestTreeViewHeader(self)
        self.apply_background_color_on_windows(self.__header)
    
    def __init_special_attributes(self):
        """
        Initializes the special attributes of the treeview.
        """
        self.__max_lines = 1 # le nombre de lignes de la ligne la plus longue de la treeview
        self.__old_width = -1 # utilisé pour savoir si la hauteur de la treeview a changé
        self.__hovered_exception = None # l'exception test sur laquelle le curseur est en train de passer
                       
    def __init_treeview(self):
        """
        Creates the treeview widget. 
        """
        self.vert_scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, style=scrollbar_style("Vertical"))
        self.vert_scrollbar.grid(row=0, column=1, sticky=tk.NSEW, rowspan=3)
    
        self.treeview = ttk.Treeview(self,yscrollcommand=self.vert_scrollbar.set)
        rows, columns = 2, 0
        self.treeview.grid(row=rows, column=columns, sticky=tk.NSEW)
        self.vert_scrollbar["command"] = self.treeview.yview
        self.columnconfigure(columns, weight=1)
        self.rowconfigure(rows, weight=1)
        self.treeview.column("#0", anchor=tk.W, stretch=tk.YES) # configure the only tree column
        self.treeview["show"] = ("tree",)

        for color_name, color in COLORS.items():
            if color_name == "lightred": # lightred is used for background (highlighting)
                self.treeview.tag_configure(color_name, background=color)
            else:
                self.treeview.tag_configure(color_name, foreground=color)
        
        # définir un tag pour les tests en exception: il faut les souligner (underline)
        self.treeview.tag_configure(
            "exception_as_link", 
            foreground=COLORS["red"], 
            font=tk_font.Font(underline=True, weight="normal", family=get_font_family_option(), size=get_font_size_option())
        )
        # définir un tag pour les tests en exception survolé: il faut les souligner (underline) et les mettre en gras (bold)
        self.treeview.tag_configure(
            "exception_hovered", 
            foreground=COLORS["red"], 
            font=tk_font.Font(underline=True, weight="bold", family=get_font_family_option(), size=get_font_size_option())
        )

        # définir un style par défault pour la treeview
        self.style = ttk.Style()
        self.style_mapping = self.style.map('Treeview')
        self.__update_tree_font(get_font_family_option(), get_font_size_option())
        
        self.treeview.tag_bind(CLICKABLE_TAG, "<<TreeviewSelect>>", self._on_select)
        self.treeview.tag_bind("nonClickable", "<<TreeviewSelect>>", self._remove_highlight_selection_effect)
        self.treeview.bind("<Motion>", self._on_hover_exception_test)
        self.treeview.bind("<Configure>", self.__wrap_tree_content) # Here we handle the motion event of the treeview 
        self.workbench.bind("UICommandDispatched", self.listen_to_update_font_commands, True) 
    
    def apply_background_color_on_windows(self, tk: ttk.Frame, color:str=BACKGROUND_COLOR_WIN_NAME):
        """
        Applies the background color on the header of the treeview.

        Args:
            tk (ttk.Frame): the header of the treeview.
            color (str): the color to apply on the header of the treeview.

        Note: This function is used only on Windows OS.
        """
        # si on est sous windows, on doit avoir un background gris pour le header de la treeview
        if os.name == "nt":
            getLogger(__name__).info("Operating system [Windows] detected. Setting the header background to gray.")
            s = ttk.Style()
            s.configure('My.TFrame', background=COLORS[color])
            tk.configure(style='My.TFrame')

    def update_font(self, event=None):
        """
        This is the handler of the `Update the font` option.  
        
        It updates the font size of the treeview if and 
        only if the font is changed in thonny.
        """          
        self.__header.resize_header_bar()
        # on applique la nouvelle police pour la treeview
        self.observe_font_changing()
     
    def _on_hover_exception_test(self, event):
        """
        Handles the motion event of the treeview. When the cursor is hovering over an exception test, 
        the font of the test is changed to bold and underlined. The cursor is also changed to "hand".
        """
        self.treeview.tag_configure(
            "exception_hovered", 
            foreground=COLORS["red"], 
            font=tk_font.Font(underline=True, weight="bold", family=get_font_family_option(), size=get_font_size_option())
        )
        if not self.is_empty():
            item = self.treeview.identify('item', event.x, event.y)
            tags = self.treeview.item(item, "tags")
            if "exception_as_link" in tags:
                if self.__hovered_exception and self.__hovered_exception != item:
                    # If the cursor is hovering over a different item, revert the font and cursor to normal for the previously hovered item
                    prev_item = self.__hovered_exception
                    prev_tags = self.treeview.item(prev_item, "tags")
                    new_tags = tuple(tag for tag in prev_tags if tag not in ("exception_hovered", "exception_cursor"))
                    self.treeview.item(prev_item, tags=new_tags + ("exception_as_link",))
                    self.treeview.configure(cursor="")
                    self.__hovered_exception = None

                # Change the font to bold and underlined and set the cursor to "hand" when the cursor enters the row with the "exception_as_link" tag
                new_tags = tuple(tag for tag in tags if tag != "exception_as_link")
                self.treeview.item(item, tags=new_tags + ("exception_hovered", "exception_cursor"))
                self.treeview.configure(cursor="hand2")
                self.__hovered_exception = item
            elif self.__hovered_exception and self.__hovered_exception != item:
                # If the cursor is not over any "exception_as_link" item, revert the font and cursor to normal for the previously hovered item
                prev_item = self.__hovered_exception
                prev_tags = self.treeview.item(prev_item, "tags")
                new_tags = tuple(tag for tag in prev_tags if tag not in ("exception_hovered", "exception_cursor"))
                self.treeview.item(prev_item, tags=new_tags + ("exception_as_link",))
                self.treeview.configure(cursor="")
                self.__hovered_exception = None
        
    def listen_to_update_font_commands(self, event):
        command:str = event.get("command_id")
        if command.startswith("increase_font_size") or command.startswith("decrease_font_size"):
            if not self.is_empty():
                self.observe_font_changing()
    
    def observe_font_changing(self, event=None):
        """
        Changes the font of the treeview.
        """
        self.__update_tree_font(get_font_family_option(), get_font_size_option())
        self.__header.change_header_font() 
        self.__wrap_tree_content(force_wrap=True)
        if not get_option(TEXT_WRAPPING):
            self.update_row_height(self._compute_optimal_height(1))
            
        error_view:L1TestErrorView = self.workbench.get_view(L1TestErrorView.__name__)
        error_view.update_font()
    
    def __update_tree_font(self, font_family, font_size):
        """
        Applies the new font to the treeview.
        """
        self.style.configure("Treeview", justify="left", font=(font_family, font_size), wrap=tk.WORD)  
        self.treeview.tag_configure("exception_as_link", font=tk_font.Font(underline=True, family=font_family, size=font_size))
    
    def __wrap_tree_content(self, event=None, margin=NORMAL_MARGIN, force_wrap:bool=False):
        """
        This function wraps the text of treeview to follow its width. By default, when 
        the `force_wrap` argument is set to False, the wrapping is done only when the 
        width of the treeview is changed. 
        
        Set `force_wrap` to True if you want to force the wrapping even if the width of 
        the treeview doesn't changed.
        """
        widget = event.widget if event else self.treeview
        if (isinstance(widget, ttk.Treeview)): 
            view = self.workbench.get_view(self.__class__.__name__)
            if view.winfo_ismapped() :  
                if not self.is_empty() and get_option(TEXT_WRAPPING):
                    width = view.winfo_width()
                    if self.__width_is_changed(width) or force_wrap: # on ne met à jour que si la largeur de la treeview a changé     
                        self.__wrap_rows(margin)
                    self.__old_width = width
    
    def __wrap_rows(self, margin=NORMAL_MARGIN, length:int=None):
        """ Wrap the text of the treeview to follow its width. 
        
        Args:
            - margin (int): the margin between rows. Keep it to the default value. 
            - length (int): the length of the text to wrap. Indicates in 
            which length the text should be wrapped.
        """
        chars_per_pixels = (self.treeview.winfo_width() // get_font_size_option()) if not length else length
        visible_nodes = self.get_all_tree_childrens()
        longest_length = self.__update_wrapped_texts(visible_nodes, chars_per_pixels)
        new_rowheight = self._compute_optimal_height(longest_length, margin)
        self.update_row_height(new_rowheight)
    
    def __width_is_changed(self, width):
        """
        Returns True if the height of the treeview hasn't changed.
        """
        return self.__old_width != width
    
    def get_all_tree_childrens(self, get_only_opened=True):
        """
        Gets recursivly all the childrens of the given node of the treeview. 
        
        Note: This function is a generator. It yields the childrens of the given node 
        one by one. This is useful to not load all the childrens in memory at once after
        each update of the treeview.
        
        Keep this method as a generator to avoid performance issues on th GUI. 
        It's observed that thonny's IDE is more faster when the treeview is 
        updated with a generator.
        
        Args:
            get_only_opened(bool): If True, only the opened nodes will be returned.
        """
        def _all_childrens(treeview: ttk.Treeview, node: str = None):
            child = treeview.get_children(node)
            for sub_child in child:
                item = treeview.item(sub_child)
                if item["open"] or not get_only_opened:
                    yield from _all_childrens(treeview, sub_child)
                yield sub_child  
        yield from _all_childrens(self.treeview)

    @cache
    def __update_wrapped_texts(self, nodes, chars_per_pixels:int) -> int:
        """
        Met à jour le wrapping des textes des nœuds spécifiés dans la Treeview.
        Return the longest wrapped line of the treeview.
        Returns the number of lines of the longest wrapped line of the treeview.
        """
        max_lines = 1
        for node in nodes:
            text = self.treeview.item(node, "text")
            wrapped_text = wrap(text, chars_per_pixels)
            
            num_lines = wrapped_text.count("\n") + 1
            if num_lines > max_lines:
                max_lines = num_lines
                
            self.treeview.item(node, text=wrapped_text)
            
        self.__max_lines = max_lines
        return max_lines
    
    def _compute_optimal_height(self, max_lines:int=None, margin=NORMAL_MARGIN):
        """
        Uses the default font metrics to calculate the optimal row height.
        The default font metrics is multiplied by the given `max_lines`.
        
        Args:
            max_lines(int): The number of lines of the longest row in the treeview.
        Return:
            (int): The new height.
        """
        row_height = get_font_size_option() * 2     # multiply by 2 to handle the line spacing
        opt_height = max_lines * (row_height * margin) if max_lines else row_height
        return round(opt_height)
    
    def update_tree_contents(self, parent="", clear_errorview=True, clear_header=True):
        """
        This function contructs and inserts the rows into the treeview.
        """
        self.__old_width = self.workbench.get_view("L1TestTreeView", False).winfo_width() if self.__old_width > 0 else -1
        
        self._restore_row_selection_effect() 
        self.clear_tree(clear_all=clear_header, clear_errorview=clear_errorview)
    
        if not self.__check_if_editor_is_open():
            return
        
        if not self._l1test_module.has_l1doctests():
            self.__header.insert(NO_TEST_FOUND_MSG, image="verdict_warning.png", clear=True, tags=("orange",))
            return
        
        self.enable_menu()
        self.__add_verdicts_to_treeview(self._l1test_module.get_l1doctests(), parent)
        
        # on insère le summarize dans le header bar que si la treeview n'est pas vide
        if not self.is_empty() and clear_header:
            # We build the summarize object 
            summarize: Summarize = self._l1test_module.get_summarize()
            # We insert the summarize infos into the header bar of the treeview
            self.insert_summarize_in_header_bar(summarize, self.__header.get_header_bar())
            self.__header.change_header_font() 
        
        self.update_row_height()
    
    def update_row_height(self, rowheight:int=None):
        """
        Updates the height of a row in the treeview.
        """
        current_row_height = self._compute_optimal_height(1) if not get_option(TEXT_WRAPPING) else self.get_current_rowheight()
        rowheight = rowheight if rowheight else current_row_height
        self.style.configure("Treeview", rowheight=rowheight) 
    
    def get_current_rowheight(self):
        """
        Returns the current height of a row in the treeview.
        """
        return self.style.lookup("Treeview", 'rowheight')
    
    def __add_verdicts_to_treeview(self, l1doctests:List[L1DocTest], parent=""):        
        for l1doctest in l1doctests:
            current_node = self._add_node_to_tree(l1doctest, parent)
            if l1doctest.has_flag(L1DocTestFlag.EMPTY):
                self.treeview.item(current_node, open=False) # on force la fermeture des fonctions vides
                self.treeview.insert(current_node, "end", text=NO_TEST_FOUND_MSG, tags=("nonClickable", l1doctest.get_flag().get_color()), 
                                     values=[l1doctest.get_node_lineno(), l1doctest.get_flag()])
            else:    
                self._add_verdicts_to_node(current_node, l1doctest.get_test_examples())
         
        self.__wrap_tree_content()
    
    def _add_node_to_tree(self, l1doctest: L1DocTest, parent=""):  
        flag: L1DocTestFlag = l1doctest.get_flag()
        open = flag.is_failing() if get_option(EXPAND_ONLY_RED_FUNCTIONS) else not get_option(FOLD_ALL_FUNCTIONS)
        return self.treeview.insert(parent, "end", text=l1doctest.get_ui_name(), values=[l1doctest.get_node_lineno(), flag],
                                tags=(CLICKABLE_TAG), image=get_photoImage(flag.get_gui_format()), open=open)
     
    def _add_verdicts_to_node(self, current_node:str, examples:list[Example]):
        """ 
        This function adds to the treeview all the rows that correspond to the given ast node.
        """
        verdicts_map = {
            FailedVerdict: (CHIP_RED, False), # False means that the verdict is not an exception
            ExceptionVerdict: (CHIP_EXCEPTION, True),
            PassedVerdict: (CHIP_GREEN, False),
        }

        for example in examples:
            verdict = example.get_verdict()
            verdict_tags = (verdict.get_color(), CLICKABLE_TAG)
            item_text = str(verdict)

            for verdict_type, (icon, is_exception) in verdicts_map.items():
                if isinstance(verdict, verdict_type):        
                    values = [verdict.get_lineno(), verdict.__class__.__name__]
                    if is_exception:
                        # on stocke le message de l'exception pour pouvoir le récupèrer au moment du clic sur le test en erreur
                        values += [verdict.get_details()] 
                        verdict_tags += ("exception_as_link", "lightred" if get_option(HIGHLIGHT_EXCEPTIONS) else "")
                    # on insère le test dans la treeview   
                    current_test = self.treeview.insert(current_node, "end", text=item_text, values=values, 
                                                    tags=verdict_tags, image=get_photoImage(icon), open=get_option(EXPAND_ONLY_RED_FUNCTIONS))
                    # on configure les tags pour insérer les détails de l'exception
                    if isinstance(verdict, FailedVerdict):
                        verdict_tags = (verdict.get_color(), "nonClickable")

                    if not is_exception: # les détail d'une exception ne sont plus insérés dans la treeview
                        for line in verdict.get_details().splitlines():
                            self.treeview.insert(current_test, "end", text=line, values=values, tags=verdict_tags)
                    break
             
    def __check_if_editor_is_open(self) -> bool:
        """
            Returns True if an editor is already opened in thonny. 
            Otherwise, returns False 
        """
        return False if not self.workbench.get_editor_notebook().get_current_editor() else True
        
    def insert_summarize_in_header_bar(self, summarize:Summarize, header: tktextext.TweakableText):
        """
        Builds the summarize test to be inserted in the header of the treeview.
        
        Args:
            summarize (Summarize): a named tuple that contains the summarize infos.
            view (tktextext.TweakableText): the header bar of the treeview.
        """
        header.direct_insert("end", "%s: %s\n" % (tr("Tests run"), summarize.total))
        
        fields_colors = {"success": "green", "failures": "darkred", "errors": "darkred", "empty": "orange"}        
        for field in summarize._fields[1:]:
            header.direct_insert("end", tr(field.capitalize()) + ": ", tags=(fields_colors[field.lower()],)) 
            value = getattr(summarize, field) # returns the value of the field
            header.direct_insert("end", f"{value}, " if summarize._fields[-1] != field else f"{value}")
                
    def clear_tree(self, clear_verdicts_data=False, clear_all=True, clear_errorview=False, disable_btns=True):
        """Clears the treeview by deleting all items. This method is called by
        the `update_tree_contents` method to clear the treeview before inserting
        the new rows.
        
        Note: this method is also called when the button `clear` is clicked. In 
        this case, the `event` is not None, then the list of l1doctests
        will be cleared. Finally, the treeview or/and header or/and the errorview 
        will be cleared.
        
        Args:
            clear_verdicts_data: If true, the l1doctests will be cleared.
            This argument is set to True when the button `clear` is clicked.
            clear_all: If True, the treeview and its header will be cleaned.
            clear_errorview: if True, the error view will be cleaned.   
            disable_btns: if True, the buttons on the header bar of the treeview will be disabled.         
        """
        if clear_verdicts_data: # si l'event est déclenché par le bouton `clear` alors on vide les listes
            from thonnycontrib.frontend import get_l1test_gui_runner
            self._l1test_module.clear()
            clear_errorview = True
            get_l1test_gui_runner().set_has_exception(False)
        if clear_all:
            self.__header.clear_header_bar()  # on supprime le contenu du header
        if clear_errorview:
            error_view:L1TestErrorView = self.workbench.get_view(L1TestErrorView.__name__)
            error_view.clear()
        self.treeview.delete(*self.treeview.get_children())
        self.__init_special_attributes()
        if disable_btns:
            self.disable_header_buttons()
    
    def _remove_highlight_selection_effect(self, event=None):
        """
        This function remove the selection effect. When a treeview's row is selected
        it removes the highlight effect on the selected row. So the selected row 
        will look like it is not selected.
        """
        self.style.map('Treeview', background=[], foreground=[])
    
    def _highlight_line_on_editor(self, lineno:int, editor: CodeView):
        """Highlights the line in the editor that corresponds to the selected row in the treeview.

        Args:
            lineno (int): the line number to highlight.
            editor (CodeView): the editor where the line will be highlighted.
        """
        index = editor.text.index(str(lineno) + ".0")
        editor.text.see(index)  # make sure that the double-clicked item is visible
        editor.text.select_lines(lineno, lineno)
    
    def _restore_row_selection_effect(self):
        """
        This function show the selection effect. When a treeview's row is selected
        it shows the highlight effect on the selected row. 
        """
        self.style.map('Treeview', 
                       background=[('selected', 'focus', '#ADD8E6'), ('selected', '!focus', '#D3D3D3')], 
                       foreground=[('selected', 'focus', 'black'), ('selected', '!focus', 'black')])
    
    def _on_select(self, event=None):
        """
        When a row is selected this function will be triggered. This function highlights 
        the line in the editor that corresponds to the seelcted row in the treeview. 
        """
        self._restore_row_selection_effect()
        editor = self.workbench.get_editor_notebook().get_current_editor()
        
        if editor:
            code_view = editor.get_code_view()
            focus = self.treeview.focus()
            if not focus: 
                return

            item = self.treeview.item(focus)
            values = item["values"]
            if not values:
                return
                
            if ExceptionVerdict.__name__ in values:
                self._report_exception_details_on_errorview(BackendException(values[-1]), error_title=item["text"])
                self.treeview.focus_set()
                        
            self._highlight_line_on_editor(values[0], code_view)
    
    def _report_exception_details_on_errorview(self, exception:Exception, error_title:str, force=True, show_treeview=True):
        """ 
        This function is called when the user clicks on an exception in the treeview. Then, 
        the error view is displayed with the details of the clicked exception. 
        
        - `show_treeview=True` means that the errorview will be displayed side by side with the treeview.
        - `force=True` means that the errorview will be forced to be visible on the thonny's GUI.
        """
        from thonnycontrib.frontend import get_l1test_gui_runner
        exception_response: ExceptionResponse = ExceptionResponse(exception)
        exception_response.set_title(error_title)
        get_l1test_gui_runner().display_error_on_view(exception_response, force, show_treeview)
    
    def enable_or_disable_text_wrapping(self):
        """
        Enable or disable the text wrapping feature.
        """
        set_option(TEXT_WRAPPING, not get_option(TEXT_WRAPPING)) # on modifie l'option par sa valeur opposée
        # une très grande longueur de texte pour empêcher le wrapping
        self.__wrap_rows() if get_option(TEXT_WRAPPING) else self.__wrap_rows(length=10**100)   
        # on configure le texte du header pour qu'il suit ou non la largeur de la treeview
        self.get_header().get_header_bar().configure(wrap=("word" if get_option(TEXT_WRAPPING) else "none"))
    
    def insert_in_header(self, text, image:str|tk.PhotoImage=None, clear=False, tags=tuple()):
        """ 
        Inserts text in the header of the treeview. 
        
        Args:
            text: the text to insert
            image: the basename with it's extension of an image to insert. 
            For example: "info.png". The image must be in the folder `/img`.
            clear: if True, the header will be cleared before inserting the text
            tags: the tags to apply to the text. For example: ("red",)
        """
        self.__header.insert(text, image, clear, tags)
    
    def disable_header_buttons(self):
        """disable the menu button of the treeview"""
        self.__header.disable_buttons()
        
    def enable_menu(self):
        """enable the menu button of the treeview"""
        self.__header.enable_buttons()
          
    def is_empty(self):
        return len(self.treeview.get_children()) == 0 
    
    def hide_view(self):
        self.workbench.hide_view(self.__class__.__name__)
    
    def show_view(self):
        self.workbench.show_view(self.__class__.__name__)
        
    def set_l1test_module(self, l1test_module: L1TestModule):
        self._l1test_module = l1test_module
    
    def get_l1test_module(self):
        """ Returns the L1test module that contains all the evaluated l1doctests. """
        return self._l1test_module
    
    def get_treeview(self):
        return self.treeview
    
    def get_header(self):
        return self.__header
    
    def get_max_lines(self):
        return self.__max_lines


# ######################################################### #
# The header of the treeview is extracted in a separate class 
# to avoid cluttering the L1TestTreeView class.
# ######################################################### #
@tostring  
class L1TestTreeViewHeader(ttk.Frame):
    """
    This class represents the header bar of the l1testTreeview. The header shows the 
    number of the run tests and the success/failed/empty tests. In addition, the header
    contains the menu button. All the functions of the menu are handled by this class.
    """
    def __init__(self, l1test_treeview: L1TestTreeView=None) -> None:
        super().__init__(l1test_treeview, style="ViewToolbar.TFrame")
        self.__l1test_treeview: L1TestTreeView = l1test_treeview
        
        self._init_special_attributes()
        self._init_header()
        
        thonny.get_workbench().bind("<Alt-i>", self.increase_row_height, True)
        thonny.get_workbench().bind("<Alt-d>", self.decrease_row_height, True)
        thonny.get_workbench().bind("<Alt-f>", self.__l1test_treeview.update_font, True)
        thonny.get_workbench().bind("<Alt-u>", self.expand_rows, True) 
        thonny.get_workbench().bind("<Alt-o>", self.fold_rows, True)
        thonny.get_workbench().bind("<Alt-r>", self.restore_original_order, True)
        thonny.get_workbench().bind("<Alt-w>", self.enable_or_disable_text_wrapping, True)
        
        thonny.get_workbench().bind("<<NotebookTabChanged>>", self.__enable_rerun_failures_button, True)
    
    def _init_header(self, row=0, column=0):
        """
        Initialize the header of the treeview. Initially, the header contains 
        only a `menu button` at the top right of the treeview. The options of the 
        menu are created by `post_button_menu()` method.

        Args:
            row (int): Always set to 0. Defaults to 0.
            column (int): Always set to 0. Defaults to 0.
        """
        self.menu = tk.Menu(self, name="menu", tearoff=False)

        self.grid(row=row, column=column, sticky="nsew")
        
        style = ttk.Style()
        style.configure("My.TFrame", background=COLORS[BACKGROUND_COLOR_WIN_NAME])
        # ajout de la zone des buttons dans le header bar
        self.__button_frame = ttk.Frame(self, style="My.TFrame")
        self.__button_frame.grid(row=0, column=0, sticky="e")
        
        self.menu_button = self.add_button(label="Menu", image=get_photoImage(BTN_MENU_TREEVIEW), command=self.post_button_menu)
        self.rerun_failure_button = self.add_button(label=tr("Rerun red tests"), image=get_photoImage(BTN_RERUN_FAILURES), command=self.rerun_failed_tests)
        
        # placer les buttons dans le header bar avec l'ordre de leurs ajout (de droite à gauche)
        frame_buttons = self.__button_frame.winfo_children()
        for index, button in enumerate(reversed(frame_buttons)):
            button.grid(row=0, column=index, sticky="e")
        
        # ajout de la zone de texte dans le header bar
        background_color = COLORS[BACKGROUND_COLOR_WIN_NAME] if os.name == "nt" else ui_utils.lookup_style_option("ViewToolbar.TFrame", "background")
        self.__text_frame = tktextext.TweakableText(
            self,
            borderwidth=0,
            relief="flat",
            height=1,
            wrap="word" if get_option(TEXT_WRAPPING) else "none",
            padx=ui_utils.ems_to_pixels(0.6),
            pady=ui_utils.ems_to_pixels(0.5),
            insertwidth=0,
            highlightthickness=0,
            background=background_color
        )
        self.__text_frame.grid(row=1, column=0, sticky="nsew")
        for color_name, color in COLORS.items():
            self.__text_frame.tag_configure(color_name, foreground=color)
        self.__text_frame.set_read_only(True)
        self.__text_frame.bind("<Configure>", self.resize_header_bar, True)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.disable_buttons()
     
    def _init_special_attributes(self):
        self._button_column = 0 # the column where the next button will be added in the header bar
        
        # Structure pour stocker les lignes détachées de la treeview. La structure est {"child_iid": ("parent_iid", index)}. 
        # Utilisé quand on trie/filtre les lignes de la treeview pour pouvoir les réinsérer dans leur ordre initial.
        self.__detached_rows: Dict[str, Tuple[str, int]] = {} 
        
        # Use a dict to map the function/verdicts to their index in the treeview. Used to retrieve the initial order of the l1doctests.
        # The keys are the lineno of the l1doctests/examples and the values are their index in the treeview.
        l1doctests = self.__l1test_treeview.get_l1test_module().get_l1doctests()
        self._index_map_row = {ld.get_node_lineno(): index for index, ld in enumerate(l1doctests)}
        self._index_map_row.update({ex.lineno: index for ld in l1doctests for index, ex in enumerate(ld.get_test_examples())})
    
    def add_button(self, command, text="", label="", image=None, width=3):
        """
        Adds a button to the header of the treeview. Each button is placed side by side (from right to left)
        in the header. Each button is separated from the other by a distance of `padx` (by default 0.07 px). 
        
        Args:
            command: the function to call when the button is clicked.
            text: the text to display on the button.
            label: the label to display when the cursor is hovering over the button.
            image: the image to display on the button. When the image is provided, the text is not displayed. 
            Add the `compound=tk.LEFT` argument on the created Button to display the image and the text.
            width: the width of the button. Set always to 3 (more than 3 will cause the button to be too large).
            padx: the distance between the buttons. The value should be between 0 and 1.
            It is recommended to give a value under 0.1 otherwise the buttons will be too far from each other.
            
        Returns:
            ttk.Button: the created button.
        """
        style = ttk.Style()
        style.configure("My.TButton", background=COLORS[BACKGROUND_COLOR_WIN_NAME])
        button = ttk.Button(self.__button_frame, text=text, command=command, image=image, width=width, style="My.TButton")
        if label:
            ui_utils.create_tooltip(button, label) 
        
        return button
       
    def post_button_menu(self):
        """
        The handler of the menu button located in the header of the treeview.
        When clicking the menu button a popoup is opened and shows several options.
        """
        self.add_menu_options()
        self.menu.tk_popup(
            self.menu_button.winfo_rootx(),
            self.menu_button.winfo_rooty() + self.menu_button.winfo_height(),
        )
    
    def add_menu_options(self):
        """
        Adds the options inside the menu button.
        """
        self.menu.delete(0, "end") 
        
        l1testModule = self.__l1test_treeview.get_l1test_module()
        disable_only_red_option = "normal" if l1testModule.is_failing() and (l1testModule.count_success() > 0 or l1testModule.count_empty() > 0) else "disabled"
        disable_restore_option = "disabled" if not self.__detached_rows else "normal"
        self.menu.add_command(label=SHOW_ONLY_RED_TESTS, command=self.show_only_red_tests, image=get_photoImage(MENU_FILTER_TESTS), compound=tk.LEFT, state=disable_only_red_option)
        self.menu.add_command(label=PLACE_RED_TEST_ON_TOP_LABEL, command=self.sort_by_red_tests, image=get_photoImage(MENU_SORT_RED_TESTS), compound=tk.LEFT, state=disable_only_red_option)
        self.menu.add_command(label=RESTORE_ORIGINAL_ORDER, command=self.restore_original_order, image=get_photoImage(MENU_RESTORE_ORIGINAL_ORDER), accelerator="Alt+r", compound=tk.LEFT, state=disable_restore_option)
        self.menu.add_separator()    
        self.menu.add_command(label=EXPAND_ALL, command=self.expand_rows, accelerator="Alt+u", image=get_photoImage(MENU_EXPAND_ROWS), compound=tk.LEFT)
        self.menu.add_command(label=FOLD_ALL, command=self.fold_rows, accelerator="Alt+o", image=get_photoImage(MENU_FOLD_ROWS), compound=tk.LEFT)
        self.menu.add_separator() 
        self.menu.add_command(label=UPDATE_FONT_LABEL, command=self.__l1test_treeview.update_font, accelerator="Alt+f", image=get_photoImage(MENU_POLICE), compound=tk.LEFT)
        self.menu.add_command(label=INCREASE_SPACE_BETWEEN_ROWS, command=self.increase_row_height, accelerator="Alt+i", image=get_photoImage(MENU_INCREASE_ROW_HEIGHT), compound=tk.LEFT)
        self.menu.add_command(label=DECREASE_SPACE_BETWEEN_ROWS, command=self.decrease_row_height, accelerator="Alt+d", image=get_photoImage(MENU_DECREASE_ROW_HEIGHT), compound=tk.LEFT)
        self.menu.add_command(label=WORD_WRAP, command=self.enable_or_disable_text_wrapping, 
                              image=get_photoImage(BOX_CHECKED) if get_option(TEXT_WRAPPING) else get_photoImage(BOX_UNCHECKED), 
                              accelerator="Alt+w", compound=tk.LEFT)
        self.menu.add_separator()
        self.menu.add_command(label=CLEAR, command=partial(self.__l1test_treeview.clear_tree, clear_verdicts_data=True), image=get_photoImage(MENU_CLEAR), compound=tk.LEFT)
    
    def rerun_failed_tests(self):
        """
        Looks if there's any failed `L1Doctest` then try to rerun them.
        """
        from thonnycontrib.frontend import get_l1test_gui_runner
        l1test_module = self.__l1test_treeview.get_l1test_module()
        
        failed_tests = l1test_module.get_l1doctests_by_flag(L1DocTestFlag.FAILED)
        if failed_tests:
            get_l1test_gui_runner().run_failed_tests() 
        
    def insert(self, text, image:str|tk.PhotoImage=None, clear=False, tags=tuple()):
        """ 
        Inserts text in the header of the treeview. 
        
        Args:
            text: the text to insert
            image: the basename with it's extension of an image to insert. 
            For example: "info.png". The image must be in the folder `/img`.
            clear: if True, the header will be cleared before inserting the text
            tags: the tags to apply to the text. For example: ("red",)
        """
        if clear:
            self.__text_frame.direct_delete("1.0", tk.END)
        if image:
            if isinstance(image, str):
                image = get_photoImage(image)
            self.__text_frame.image_create(tk.END, image=image)
            text = " " + text # add a space after the image
        self.__text_frame.direct_insert(tk.END, text, tags=tags)
        self.resize_header_bar()
        
    def resize_header_bar(self, event=None):
        """ 
        Resize the height of the header. 
        Always keep this method otherwise the header will take the whole treeview.
        """
        height = self.tk.call((self.__text_frame, "count", "-update", "-displaylines", "1.0", "end"))
        self.__text_frame.configure(height=height)
    
    def __is_red_test(self, item_values):
        """
        Check if the test is a "red test" based on the provided values.
        """
        return any(verdict.__name__ in item_values for verdict in RED_VERDICTS) or str(L1DocTestFlag.FAILED) in item_values
     
    def sort_by_red_tests(self):  
        """
        Sort the treeview by red tests. The red tests will be placed on top of the treeview.
        """     
        treeview = self.__l1test_treeview.get_treeview()
        for child in self.__l1test_treeview.get_all_tree_childrens(get_only_opened=False):
            item = treeview.item(child)  
            # Check if any of the red_verdicts is in the item values
            if not self.__is_red_test(item["values"]):
                parent = treeview.parent(child) 
                self.__detached_rows[child] = (parent, self.__get_item_index(item))
        for child, (parent, _) in self.__detached_rows.items():
            treeview.move(child, parent, "end")     
            
    def show_only_red_tests(self):
        """
        When invoking this method the treeview will show only the red rows.
        """
        treeview = self.__l1test_treeview.get_treeview()
        for child in self.__l1test_treeview.get_all_tree_childrens(get_only_opened=False):
            item = treeview.item(child)
            # Check if any of the red_verdicts is in the item values
            if not self.__is_red_test(item["values"]):
                self.__detached_rows[child] = (treeview.parent(child), self.__get_item_index(item))
        treeview.detach(*self.__detached_rows.keys())
        
    def restore_original_order(self, event=None):
        """
        When invoking this method the treeview will restore the original order of its rows.
        This function is useful when the treeview is sorted by red tests or when it shows only the red tests.
        """
        for child, (parent, index) in self.__detached_rows.items():
            self.__l1test_treeview.get_treeview().move(child, parent, index)
        self.__detached_rows.clear()
       
    def __get_item_index(self, item):
        """
        Get the index of the given item in the treeview. The function retrieves the index of the item 
        in the `self._index_map_row` dictionary. If the item is not found, it returns 0.
        
        Args:
            item: the item to get its index. The item should be a dict.
            You can got the dict by using the method `treeview.item(child)`.
        """        
        values_set = set(item["values"]) # les lineno sont stockés dans item["values"]
        for value in values_set:
            index = self._index_map_row.get(value)
            if index is not None:
                return index
        # If no match is found, return 0 probably it's a en empty function (without tests)
        return 0
        
    def expand_rows(self, event=None): 
        """ Spreads the rows of the functions in the treeview """
        treeview = self.__l1test_treeview.get_treeview()
        for child in treeview.get_children():
            item = treeview.item(child)
            if str(L1DocTestFlag.EMPTY) not in item["values"]: # on n'ouvre pas les fonctions vides
                treeview.item(child, open=True)
            
    def fold_rows(self, event=None):
        """ Folds the rows of the functions in the treeview """
        treeview = self.__l1test_treeview.get_treeview()
        for child in treeview.get_children():
            treeview.item(child, open=False)
    
    def increase_row_height(self, event=None):
        """
        Increases the height of a row in the treeview.
        
        Args: 
            event: the event that triggered this method.
        """
        if not self.__l1test_treeview.is_empty():
            current_height = self.__l1test_treeview.get_current_rowheight()
            self.__l1test_treeview.update_row_height(current_height+1)
    
    def decrease_row_height(self, event=None):
        """
        Decreases the height of a row in the treeview.
        
        Args: 
            event: the event that triggered this method.
        """
        if not self.__l1test_treeview.is_empty():
            current_height = self.__l1test_treeview.get_current_rowheight()
            max_lines = self.__l1test_treeview.get_max_lines()
            opt = self.__l1test_treeview._compute_optimal_height(max_lines, SMALL_MARGIN)
            if current_height > opt:
                self.__l1test_treeview.update_row_height(current_height-1) 
    
    def enable_or_disable_text_wrapping(self, event=None):
        """Enable or disbale the text wrappin on the treeview."""
        self.__l1test_treeview.enable_or_disable_text_wrapping()
        
    def clear_header_bar(self):
        """Clears the header of the treeview."""
        self.__text_frame.direct_delete("1.0", "end")
        self.resize_header_bar()
        self._init_special_attributes()
        
    def change_header_font(self, header_font_size=11):
        """
        Changes the font size of the header bar of the treeview.

        Args:
            header_font_size (int, optional): The header font size. Defaults to 11.
        """
        self.__text_frame.config(font=(get_font_family_option(), header_font_size))
        self.resize_header_bar()
    
    def disable_buttons(self):
        """disable the menu button of the treeview"""
        self.disable_menu_button()
        self.disable_rerun_button()
        
    def enable_buttons(self):
        """enable the menu button of the treeview"""
        self.menu_button.state(["!disabled"])
        # enable rerun_failures_button only if there's any failed test
        self.__enable_rerun_failures_button()
        
    def disable_menu_button(self, event=None):
        """disable the menu button of the treeview"""
        self.menu_button.state([tk.DISABLED])
        
    def disable_rerun_button(self, event=None):
        """disable the rerun button of the treeview"""
        self.rerun_failure_button.state([tk.DISABLED])
       
    def __enable_rerun_failures_button(self, event=None) -> bool:
        """
        Enable the `rerun_failures_button` only if there's any failed test. 
        This function is called when the current editor is changed, if the current
        script is not saved or if the current script is not the same as the script
        that has been run by `L1test`, the button will be disabled.
        
        Note: Remember that the `rerun_failures` button should be accessible only after
        the execution of the `L1test`. In addition, it cannot be enabled when 
        the user changed the script that has been run by `L1test`.
        
        Returns:
            bool: True if the button is enabled. Otherwise, returns False.
        """
        current_filename = editors.get_saved_current_script_filename(force=False)

        l1test_module = self.__l1test_treeview.get_l1test_module()
        # Disable the button if the current script is not saved or if it's not the same as the script that has been run by L1test
        has_failed_flag = l1test_module.does_flag_exist(L1DocTestFlag.FAILED)
        if not current_filename or l1test_module.get_filename() != current_filename: 
            state = tk.DISABLED
        elif not has_failed_flag: 
            state = tk.DISABLED # disable the button if there's no failed tests
        else:
            state = "!disabled"

        self.rerun_failure_button.state([state])
        return state == "!disabled"
     
    def is_header_bar_cleared(self): 
        return not self.__text_frame.get("1.0", tk.END).strip("\n")   
    
    ## Getters ##
    def get_header_bar(self):
        return self.__text_frame
    
    def get_menu_button(self):
        return self.menu_button
    
    def get_menu(self):
        return self.menu
    
    def get_treeview(self):
        return self.__l1test_treeview
from collections import namedtuple
from rich.console import Console
from thonnycontrib.frontend import get_l1test_cli_runner
from thonnycontrib.frontend.gui.outlines_menu.l1test_outliner_menu import L1TestOutliner
from thonnycontrib.exceptions import CliException
import os, argparse
from rich.theme import Theme
from rich.style import Style

__CONSOLE_DEFAULT_THEME = {
    "repr.str": "white", 
    "repr.path": Style(color="magenta")
}

CONSOLE = Console(theme=Theme(__CONSOLE_DEFAULT_THEME, inherit=False))

def __load_source_from_filename(filename:str):
    SourcePath = namedtuple('SourcePath', ["filename", "source"])
    # Normaliser le chemin du fichier
    abs_filename = os.path.abspath(filename.strip())
    
    with open(filename, "r") as src_io:
        source = src_io.read()
    
    return SourcePath(abs_filename, source)

def parse_args():
    print("L1Test-CLI: Command Line Interface for L1Test\n")
    parser = argparse.ArgumentParser(
                        prog="L1Test-CLI", 
                        description="L1Test-CLI allows to execute the tests of a given filename")
    parser.add_argument("filename", help="path to the python file")
    parser.add_argument("-p", "--pretty", action="store_true", help="Prints a colored result instead of black/white mode.")
    parser.add_argument("-l", "--list", action="store_true", help="list all the functions/classes of the given file. Each listing is preceded by its line number.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Shows the execution state. It shows the current executed test line.")
    
    return parser.parse_args()

def outline(source:str):
    nodes = L1TestOutliner.parse(source)
    mapped_to_str = [f"({node.get_type().get_cli_repr()}) {node.get_lineno()}: {node.get_name()}" for node in nodes] 
    return "\n".join(mapped_to_str)

def parse_linenos(input:str):
    try:
        # Diviser la chaîne en une liste de chaînes représentant les nombres
        numbers_as_strings = input.split()

        # Convertir chaque chaîne en un nombre entier
        numbers = [int(num) for num in numbers_as_strings]

        return numbers
    except ValueError:
        raise ValueError("Erreur : nombres invalides. All the tests will be executed.\n\n")


# la syntaxe python3 -m l1test-cli <fichier>
def main():
    args = parse_args()
    output = ""
    try:
        sourcePath = __load_source_from_filename(args.filename)  
        selected_linenos = []
        if (args.list) :
            outlines = outline(sourcePath.source)              
            input = input(outlines+"\n* Enter the functions you want to test (ex: 1 2 3): ") 
            try:
                selected_linenos = parse_linenos(input)
            except ValueError as e:
                output += str(e) 

        cli_runner = get_l1test_cli_runner() 
        cli_runner.set_filename(sourcePath.filename)
        cli_runner.set_source(sourcePath.source)
        cli_runner.get_evaluator() 
        cli_runner.set_pretty_mode(args.pretty)
        cli_runner.set_show_exec_state(args.verbose)
        
        if selected_linenos:
            cli_runner.run_test_at(selected_linenos)
        else:
            cli_runner.run()
    except CliException as e:
        output = str(e)

    CONSOLE.print(output) if args.pretty else print(output)

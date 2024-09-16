# Auteur : Reda ID TALEB

from setuptools import setup

# Le chemin vers le programme qui lance le l1test en mode CLI
L1TEST_CLI_MAIN = "thonnycontrib.frontend.cli.command_line:main"
# Le nom de la commande à exécuter dans le terminal
L1TEST_CLI_COMMAND = "xpycli"

setup(
    name=L1TEST_CLI_COMMAND,
    version="1.0",
    author="Reda ID-TALEB",
    description="This is a command line based tool to run tests on your python code",
    long_description="This is a command line based tool to run tests on your python code",
    platforms=["Windows", "macOS", "Linux"],
    python_requires=">=3.9",
    scripts=["cli-scripts/l1test"],
)

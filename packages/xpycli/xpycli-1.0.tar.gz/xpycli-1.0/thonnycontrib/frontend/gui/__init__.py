# Ceci est une implémentation de création d'un singleton pour OutlineParser
_outliner = None

def get_outliner():
    """
    Retourne une instance de `OutlineParser` en tant que singleton.
    """
    from .outlines_menu.l1test_outliner_menu import L1TestOutliner
    return L1TestOutliner() if not _outliner else _outliner
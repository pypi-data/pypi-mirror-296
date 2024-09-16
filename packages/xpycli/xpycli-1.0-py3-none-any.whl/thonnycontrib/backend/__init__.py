_event_manager = None

def get_event_manager():
    """
    Retourne une instance de `OutlineParser` en tant que singleton.
    """
    from .models import EventManager
    return EventManager() if not _event_manager else _event_manager
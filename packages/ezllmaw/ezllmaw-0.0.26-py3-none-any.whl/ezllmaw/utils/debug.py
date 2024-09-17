import functools
import ezllmaw as ez

def debug_print(func, *args, **kwargs):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if ez.settings.debug == True:
            return func(*args, **kwargs)
    return wrapper

@debug_print
def ez_print(*args, **kwargs)->None:
    """Here is vanilla print."""
    print(*args, **kwargs)
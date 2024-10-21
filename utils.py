from typing import Callable, Dict
from functools import reduce

def compose(*functions: Callable) -> Callable:
    """
    Create a function composition from a sequence of functions using functools.reduce.
    """
    def composition(dict_data: Dict, *args, **kwargs) -> Dict:
        return reduce(lambda data, func: func(data, *args, **kwargs), functions, dict_data)
    return composition
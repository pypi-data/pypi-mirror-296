import inspect

def ai_function(func):
    """
    A decorator that converts a function into a function that returns its own definition as a string.

    Args:
        func: The function to decorate.

    Returns:
        A new function that returns the source code of the original function as a string.
    """

    source_code = inspect.getsource(func)
    # Remove leading whitespace but maintain indentation 
    lines = source_code.splitlines()
    indent = "    "  # Indentation for the function definition
    source_code = indent + '\n'.join(l.strip() for l in lines[1:])

    def new_func(*args, **kwargs):
        """
        A new function that returns the source code of the original function.

        Args:
            *args: The arguments passed to the original function.
            **kwargs: The keyword arguments passed to the original function.

        Returns:
            A string containing the source code of the original function.
        """
        return source_code
    return new_func
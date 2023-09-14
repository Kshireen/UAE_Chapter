""" decorators """

def handle_exceptions(func):
    """ class method decorator to handle exceptions """
    def wrapper(self, *args, **kw):
        try:
            result = func(self, *args, **kw)
            return result
        except Exception as excpt:
            raise excpt
    return wrapper


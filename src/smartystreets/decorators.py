"""Data validation decorators."""


def validate_args(f):
    """
    Ensures that *args consist of a consistent type

    :param f: any client method with *args parameter
    :return: function f
    """

    def wrapper(self, args):
        arg_types = {type(arg) for arg in args}
        if len(arg_types) > 1:
            raise TypeError("Mixed input types are not allowed")

        elif list(arg_types)[0] not in (dict, str):
            raise TypeError("Only dict and str types accepted")

        return f(self, args)

    return wrapper


def truncate_args(f):
    """
    Ensures that *args do not exceed a set limit or are truncated to meet that limit

    :param f: any Client method with *args parameter
    :return: function f
    """

    def wrapper(self, args):
        if len(args) > 100:
            if self.truncate_addresses:
                args = args[:100]
            else:
                raise ValueError(
                    "This exceeds 100 address at a time SmartyStreets limit"
                )

        return f(self, args)

    return wrapper

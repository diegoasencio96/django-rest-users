from collections import OrderedDict, namedtuple

_Field = namedtuple('_Field', [
    'name',
    'default',
    'help',
    'import_string',
])


class Field(_Field):

    def __new__(
            cls, name, *,
            default=None,
            help=None,  # pylint: disable=redefined-builtin
            import_string=False):
        return super().__new__(
            cls, name=name, default=default,
            help=help, import_string=import_string)

from typing import Optional, Type, TypeVar

class TypeSpec:
    typename: type
    structchar: (str, str)
    printmask: str

    def __init__(self, typename: type, structchar: str, printmask: str):
        self.typename = typename
        self.structchar = structchar
        self.printmask = printmask

class TypeClass:
    TUPLE: TypeSpec = TypeSpec(typename=tuple, structchar=('(', ')'), printmask='%s: %s')
    LIST: TypeSpec = TypeSpec(typename=list, structchar=('[', ']'), printmask='[%s]: %s')
    SET: TypeSpec = TypeSpec(typename=set, structchar=('{', '}'), printmask='%s')
    DICT: TypeSpec = TypeSpec(typename=dict, structchar=('{', '}'), printmask="'%s': %s")

TypeDict: dict[Type, TypeClass] = { # TypeDict is a dictionary of Type to TypeClass
    list: TypeClass.LIST,
    tuple: TypeClass.TUPLE,
    set: TypeClass.SET,
    dict: TypeClass.DICT
}
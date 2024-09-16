from typing import Optional, Type, TypeVar
from colors import Colors
from typeclasses import TypeSpec, TypeClass, TypeDict

class BetterPrint:
    __debugMode: bool = True
    __detailedPrint: bool = False
    __namedInstances: bool = False
    namedInstancesLevel: int = 0
    valueSeparatorCharacter = ','

    __indentlevel: int = 0
    indentchar: str = "  "
    colorScheme: Colors 

    def __init__(self, *, ColorScheme: Optional[Colors] = None):
        self.__debugMode = True
        self.colorScheme = ColorScheme or Colors
        self.typedicts = TypeDict

    def toggleNamedInstances(self, isNamedInstances: Optional[bool] = None):
        self.__namedInstances = isNamedInstances or not self.__namedInstances
        print(f"{self.colorScheme.WARNING}Named instances is now {self.__namedInstances}{self.colorScheme.ENDC}")

    def toggleDetailedPrint(self, isDetailedPrintMode: Optional[bool] = None):
        self.__detailedPrint = isDetailedPrintMode or not self.__detailedPrint
        print(f"{self.colorScheme.WARNING}Detailed print mode is now {self.__detailedPrint}{self.colorScheme.ENDC}")

    def toggleDebugMode(self, isDebugMode: Optional[bool] = None):
        self.__debugMode = isDebugMode or not self.__debugMode
        print(f"{self.colorScheme.WARNING}Debug mode is now {self.__debugMode}{self.colorScheme.ENDC}")

    def better_print(self, *objects, sep=' ', end='\n', flush=False, style: Colors = None):
        for obj in objects:
            self.typedprint(obj, end=sep, style=style)
        print(end=end, flush=flush)

    def debug_print(self, *objects, sep=' ', end='\n', flush=False):
        if self.__debugMode == True:
            self.better_print(*objects, sep=sep, end=end, flush=flush, style=self.colorScheme.DEBUG)

    def styledprint(
        self, 
        *objects, 
        indent: str = '',
        sep='', 
        end='\n', 
        flush=False, 
        style: Colors = None
    ):
        for obj in objects:
            if style:
                print(indent, f"{style}{obj}{self.colorScheme.ENDC}", end=sep)
            else:
                print(f"{obj}", end=sep)
        print(end=end, flush=flush)

    def typedprint(self, *objects, sep='', end='\n', flush=False, style: Colors = None):
        for obj in objects:
            if obj.__class__.__module__ != 'builtins': # check if the object is a user-defined class
                self.debug_print(f"NOT BUILTIN!")
                self.class_print(obj, end=sep)
            else: self.typespecificprint(self.typedicts.get(type(obj)), obj, end=sep, sep='\n', style=style)
        print(end=end, flush=flush)

    def class_print(self, *objects, sep='', end='\n', flush=False, style: Colors = None):
        for obj in objects:
            indent = self.indentchar * self.__indentlevel
            self.__namedInstancesLevel(
                indent=indent, 
                printObj=f"Instance of {obj.__class__.__name__} @ module '{obj.__class__.__module__}':", 
                style=style or self.colorScheme.UNDERLINE
            )

            self.styledprint(
                "{", 
                indent=indent,
                style=style or self.colorScheme.BOLD,
            )
            for attribute in dir(obj):
                if not attribute.endswith('__'):
                    self.better_print(f"{self.indentchar}{obj.__class__.__name__}.{attribute}: {getattr(obj, attribute)}", style=style or self.colorScheme.OKCYAN, sep=sep, end=sep, flush=flush)
            self.styledprint(
                "}", 
                indent=indent,
                style=style or self.colorScheme.BOLD,
            )
            print(end=sep, flush=flush)


    def __namedInstancesLevel(self, *, printObj: str, indent: str, style: Colors = None):
        if self.__namedInstances and (self.namedInstancesLevel + 1) >= self.__indentlevel: 
            self.styledprint(
                printObj, 
                indent=indent,
                style=style or self.colorScheme.UNDERLINE,
            )

    def typespecificprint(
        self,
        typeval: TypeSpec = None, 
        *obj, 
        sep: str = '',
        end: str = '\n', 
        flush: bool = False,
        style: Colors = None
    ) -> None:
        sep += '\n' if '\n' not in sep else ''
        indent = self.indentchar * self.__indentlevel

        if(typeval == None): 
            for i in obj:
                if i.__class__.__module__ != 'builtins':
                    self.class_print(i, end=sep)
                else:
                    self.styledprint(
                        f"{i}{self.valueSeparatorCharacter if self.__indentlevel > 0 else ''}",
                        indent=indent,
                        style=style or self.colorScheme.OKCYAN
                    )
        else:
            self.__indentlevel += 1

            self.__namedInstancesLevel(
                indent=indent, 
                printObj=f"Instance of {typeval.typename}:", 
                style=style or self.colorScheme.UNDERLINE
            )


            self.styledprint(
                f"{typeval.structchar[0]}", 
                indent=indent,
                style=style or self.colorScheme.BOLD
            )
            for i in obj: 
                objtype = type(i)
                if objtype == dict:
                    for key, value in i.items():
                        self.typespecificprint(None, indent, f"'{key}': {value}", sep=sep, end=end, style=style)
                        # if self.typedicts.get(type(value)) != None:
                        #     self.typespecificprint(None, self.typedicts.get(type(value)), indent, value, sep=sep, end=end)

                # elif type(i) in [str, int, float, bool]: 
                #     self.styledprint(indent, f"{self.indentchar}{i},", end=sep, style=style)
                else:
                    if objtype in [list, tuple, set]:
                        for j in i:
                            self.typespecificprint(self.typedicts.get(type(j)), j, sep=sep, end=sep, style=style)
                    else:
                        self.typespecificprint(self.typedicts.get(objtype), i, sep=sep, end=sep, style=style)
            self.styledprint(
                f"{indent}{typeval.structchar[1]}", 
                style=style or self.colorScheme.BOLD, 
                sep=sep,
                end=end, 
                flush=flush
            )
            
            self.__indentlevel -= 1

    def __str__(self):
        return f"BetterPrint({self.colorScheme})"
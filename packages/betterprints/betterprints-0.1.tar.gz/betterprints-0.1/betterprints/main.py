from betterprint import BetterPrint as bp

betterprintconfig = bp()
colors = betterprintconfig.colorScheme

def debugprint(*objects, sep=' ', end='\n', flush=False):
    betterprintconfig.debug_print(*objects, sep=sep, end=end, flush=flush)

def styledprint(*objects, sep=' ', end='\n', flush=False, style=None):
    betterprintconfig.styledprint(*objects, sep=sep, end=end, flush=flush, style=style)

def betterprint(*objects, sep=' ', end='\n', flush=False, style=None):
    betterprintconfig.better_print(*objects, sep=sep, end=end, flush=flush, style=style)

def classprint(*objects, sep=' ', end='\n', flush=False, style=None):
    betterprintconfig.class_print(*objects, sep=sep, end=end, flush=flush, style=style)
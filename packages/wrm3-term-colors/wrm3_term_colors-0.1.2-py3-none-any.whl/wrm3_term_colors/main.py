from .pallette     import pallette
from .cls          import CLR 

#<=====>#

c = CLR()

#<=====>#

def color_it(font_color, bg_color='black', bold=False, italic=False):
    """
    Returns a function that prints or returns colored text.
    """
    def color_fnc(text, print_tf=True, length=0, align='left'):
        if print_tf:
            c.color_print(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)
        else:
            return c.color_string(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)
    return color_fnc

#<=====>#

def cs(text: str, font_color: str, bg_color: str = 'black', bold: bool = False, italic: bool = False, length: int = 0, align: str = 'left') -> str:
    """
    Returns a colorized string using specified parameters.
    
    :param text: The text to be colorized.
    :param font_color: The font color (name or hex).
    :param bg_color: The background color (name or hex), default is 'black'.
    :param bold: Boolean indicating if text should be bold, default is False.
    :param italic: Boolean indicating if text should be italic, default is False.
    :param length: The length for text alignment, default is 0 (no alignment).
    :param align: Text alignment option ('left', 'center', 'right'), default is 'left'.
    :return: A string with ANSI escape codes for coloring.
    """
    return c.color_string(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)

#<=====>#

def cp(text: str, font_color: str, bg_color: str = 'black', bold: bool = False, italic: bool = False, length: int = 0, align: str = 'left') -> None:
    """
    Prints a colorized string using specified parameters.
    
    :param text: The text to be printed.
    :param font_color: The font color (name or hex).
    :param bg_color: The background color (name or hex), default is 'black'.
    :param bold: Boolean indicating if text should be bold, default is False.
    :param italic: Boolean indicating if text should be italic, default is False.
    :param length: The length for text alignment, default is 0 (no alignment).
    :param align: Text alignment option ('left', 'center', 'right'), default is 'left'.
    """
    c.color_print(text, font_color=font_color, bg_color=bg_color, bold=bold, italic=italic, length=length, align=align)

#<=====>#

K = color_it('black')
R = color_it('red')
G = color_it('green')
Y = color_it('yellow')
B = color_it('blue')
M = color_it('magenta')
C = color_it('cyan')
W = color_it('white')
LGy = color_it('light_grey')
DGy = color_it('dark_grey')
LR = color_it('light_red')
LG = color_it('light_green')
LY = color_it('light_yellow')
LB = color_it('light_blue')
LM = color_it('light_magenta')
LC = color_it('light_cyan')

#<=====>#

KoK = color_it(font_color='black', bg_color='black')
RoK = color_it(font_color='red', bg_color='black')
GoK = color_it(font_color='green', bg_color='black')
YoK = color_it(font_color='yellow', bg_color='black')
BoK = color_it(font_color='blue', bg_color='black')
MoK = color_it(font_color='magenta', bg_color='black')
CoK = color_it(font_color='cyan', bg_color='black')
WoK = color_it(font_color='white', bg_color='black')
LGyoK = color_it(font_color='light_grey', bg_color='black')
DGyoK = color_it(font_color='dark_grey', bg_color='black')
LRoK = color_it(font_color='light_red', bg_color='black')
LGoK = color_it(font_color='light_green', bg_color='black')
LYoK = color_it(font_color='light_yellow', bg_color='black')
LBoK = color_it(font_color='light_blue', bg_color='black')
LMoK = color_it(font_color='light_magenta', bg_color='black')
LCoK = color_it(font_color='light_cyan', bg_color='black')

#<=====>#

KoR = color_it(font_color='black', bg_color='red')
RoR = color_it(font_color='red', bg_color='red')
GoR = color_it(font_color='green', bg_color='red')
YoR = color_it(font_color='yellow', bg_color='red')
BoR = color_it(font_color='blue', bg_color='red')
MoR = color_it(font_color='magenta', bg_color='red')
CoR = color_it(font_color='cyan', bg_color='red')
WoR = color_it(font_color='white', bg_color='red')
LGyoR = color_it(font_color='light_grey', bg_color='red')
DGyoR = color_it(font_color='dark_grey', bg_color='red')
LRoR = color_it(font_color='light_red', bg_color='red')
LGoR = color_it(font_color='light_green', bg_color='red')
LYoR = color_it(font_color='light_yellow', bg_color='red')
LBoR = color_it(font_color='light_blue', bg_color='red')
LMoR = color_it(font_color='light_magenta', bg_color='red')
LCoR = color_it(font_color='light_cyan', bg_color='red')

#<=====>#

KoG = color_it(font_color='black', bg_color='green')
RoG = color_it(font_color='red', bg_color='green')
GoG = color_it(font_color='green', bg_color='green')
YoG = color_it(font_color='yellow', bg_color='green')
BoG = color_it(font_color='blue', bg_color='green')
MoG = color_it(font_color='magenta', bg_color='green')
CoG = color_it(font_color='cyan', bg_color='green')
WoG = color_it(font_color='white', bg_color='green')
LGyoG = color_it(font_color='light_grey', bg_color='green')
DGyoG = color_it(font_color='dark_grey', bg_color='green')
LRoG = color_it(font_color='light_red', bg_color='green')
LGoG = color_it(font_color='light_green', bg_color='green')
LYoG = color_it(font_color='light_yellow', bg_color='green')
LBoG = color_it(font_color='light_blue', bg_color='green')
LMoG = color_it(font_color='light_magenta', bg_color='green')
LCoG = color_it(font_color='light_cyan', bg_color='green')

#<=====>#

KoY = color_it(font_color='black', bg_color='yellow')
RoY = color_it(font_color='red', bg_color='yellow')
GoY = color_it(font_color='green', bg_color='yellow')
YoY = color_it(font_color='yellow', bg_color='yellow')
BoY = color_it(font_color='blue', bg_color='yellow')
MoY = color_it(font_color='magenta', bg_color='yellow')
CoY = color_it(font_color='cyan', bg_color='yellow')
WoY = color_it(font_color='white', bg_color='yellow')
LGyoY = color_it(font_color='light_grey', bg_color='yellow')
DGyoY = color_it(font_color='dark_grey', bg_color='yellow')
LRoY = color_it(font_color='light_red', bg_color='yellow')
LGoY = color_it(font_color='light_green', bg_color='yellow')
LYoY = color_it(font_color='light_yellow', bg_color='yellow')
LBoY = color_it(font_color='light_blue', bg_color='yellow')
LMoY = color_it(font_color='light_magenta', bg_color='yellow')
LCoY = color_it(font_color='light_cyan', bg_color='yellow')

#<=====>#

KoB = color_it(font_color='black', bg_color='blue')
RoB = color_it(font_color='red', bg_color='blue')
GoB = color_it(font_color='green', bg_color='blue')
YoB = color_it(font_color='yellow', bg_color='blue')
BoB = color_it(font_color='blue', bg_color='blue')
MoB = color_it(font_color='magenta', bg_color='blue')
CoB = color_it(font_color='cyan', bg_color='blue')
WoB = color_it(font_color='white', bg_color='blue')
LGyoB = color_it(font_color='light_grey', bg_color='blue')
DGyoB = color_it(font_color='dark_grey', bg_color='blue')
LRoB = color_it(font_color='light_red', bg_color='blue')
LGoB = color_it(font_color='light_green', bg_color='blue')
LYoB = color_it(font_color='light_yellow', bg_color='blue')
LBoB = color_it(font_color='light_blue', bg_color='blue')
LMoB = color_it(font_color='light_magenta', bg_color='blue')
LCoB = color_it(font_color='light_cyan', bg_color='blue')

#<=====>#

KoM = color_it(font_color='black', bg_color='magenta')
RoM = color_it(font_color='red', bg_color='magenta')
GoM = color_it(font_color='green', bg_color='magenta')
YoM = color_it(font_color='yellow', bg_color='magenta')
BoM = color_it(font_color='blue', bg_color='magenta')
MoM = color_it(font_color='magenta', bg_color='magenta')
CoM = color_it(font_color='cyan', bg_color='magenta')
WoM = color_it(font_color='white', bg_color='magenta')
LGyoM = color_it(font_color='light_grey', bg_color='magenta')
DGyoM = color_it(font_color='dark_grey', bg_color='magenta')
LRoM = color_it(font_color='light_red', bg_color='magenta')
LGoM = color_it(font_color='light_green', bg_color='magenta')
LYoM = color_it(font_color='light_yellow', bg_color='magenta')
LBoM = color_it(font_color='light_blue', bg_color='magenta')
LMoM = color_it(font_color='light_magenta', bg_color='magenta')
LCoM = color_it(font_color='light_cyan', bg_color='magenta')

#<=====>#

KoC = color_it(font_color='black', bg_color='cyan')
RoC = color_it(font_color='red', bg_color='cyan')
GoC = color_it(font_color='green', bg_color='cyan')
YoC = color_it(font_color='yellow', bg_color='cyan')
BoC = color_it(font_color='blue', bg_color='cyan')
MoC = color_it(font_color='magenta', bg_color='cyan')
CoC = color_it(font_color='cyan', bg_color='cyan')
WoC = color_it(font_color='white', bg_color='cyan')
LGyoC = color_it(font_color='light_grey', bg_color='cyan')
DGyoC = color_it(font_color='dark_grey', bg_color='cyan')
LRoC = color_it(font_color='light_red', bg_color='cyan')
LGoC = color_it(font_color='light_green', bg_color='cyan')
LYoC = color_it(font_color='light_yellow', bg_color='cyan')
LBoC = color_it(font_color='light_blue', bg_color='cyan')
LMoC = color_it(font_color='light_magenta', bg_color='cyan')
LCoC = color_it(font_color='light_cyan', bg_color='cyan')

#<=====>#

KoW = color_it(font_color='black', bg_color='white')
RoW = color_it(font_color='red', bg_color='white')
GoW = color_it(font_color='green', bg_color='white')
YoW = color_it(font_color='yellow', bg_color='white')
BoW = color_it(font_color='blue', bg_color='white')
MoW = color_it(font_color='magenta', bg_color='white')
CoW = color_it(font_color='cyan', bg_color='white')
WoW = color_it(font_color='white', bg_color='white')
LGyoW = color_it(font_color='light_grey', bg_color='white')
DGyoW = color_it(font_color='dark_grey', bg_color='white')
LRoW = color_it(font_color='light_red', bg_color='white')
LGoW = color_it(font_color='light_green', bg_color='white')
LYoW = color_it(font_color='light_yellow', bg_color='white')
LBoW = color_it(font_color='light_blue', bg_color='white')
LMoW = color_it(font_color='light_magenta', bg_color='white')
LCoW = color_it(font_color='light_cyan', bg_color='white')

#<=====>#

KoLGy = color_it(font_color='black', bg_color='light_grey')
RoLGy = color_it(font_color='red', bg_color='light_grey')
GoLGy = color_it(font_color='green', bg_color='light_grey')
YoLGy = color_it(font_color='yellow', bg_color='light_grey')
BoLGy = color_it(font_color='blue', bg_color='light_grey')
MoLGy = color_it(font_color='magenta', bg_color='light_grey')
CoLGy = color_it(font_color='cyan', bg_color='light_grey')
WoLGy = color_it(font_color='white', bg_color='light_grey')
LGyoLGy = color_it(font_color='light_grey', bg_color='light_grey')
DGyoLGy = color_it(font_color='dark_grey', bg_color='light_grey')
LRoLGy = color_it(font_color='light_red', bg_color='light_grey')
LGoLGy = color_it(font_color='light_green', bg_color='light_grey')
LYoLGy = color_it(font_color='light_yellow', bg_color='light_grey')
LBoLGy = color_it(font_color='light_blue', bg_color='light_grey')
LMoLGy = color_it(font_color='light_magenta', bg_color='light_grey')
LCoLGy = color_it(font_color='light_cyan', bg_color='light_grey')

#<=====>#

KoDGy = color_it(font_color='black', bg_color='dark_grey')
RoDGy = color_it(font_color='red', bg_color='dark_grey')
GoDGy = color_it(font_color='green', bg_color='dark_grey')
YoDGy = color_it(font_color='yellow', bg_color='dark_grey')
BoDGy = color_it(font_color='blue', bg_color='dark_grey')
MoDGy = color_it(font_color='magenta', bg_color='dark_grey')
CoDGy = color_it(font_color='cyan', bg_color='dark_grey')
WoDGy = color_it(font_color='white', bg_color='dark_grey')
LGyoDGy = color_it(font_color='light_grey', bg_color='dark_grey')
DGyoDGy = color_it(font_color='dark_grey', bg_color='dark_grey')
LRoDGy = color_it(font_color='light_red', bg_color='dark_grey')
LGoDGy = color_it(font_color='light_green', bg_color='dark_grey')
LYoDGy = color_it(font_color='light_yellow', bg_color='dark_grey')
LBoDGy = color_it(font_color='light_blue', bg_color='dark_grey')
LMoDGy = color_it(font_color='light_magenta', bg_color='dark_grey')
LCoDGy = color_it(font_color='light_cyan', bg_color='dark_grey')

#<=====>#

KoLR = color_it(font_color='black', bg_color='light_red')
RoLR = color_it(font_color='red', bg_color='light_red')
GoLR = color_it(font_color='green', bg_color='light_red')
YoLR = color_it(font_color='yellow', bg_color='light_red')
BoLR = color_it(font_color='blue', bg_color='light_red')
MoLR = color_it(font_color='magenta', bg_color='light_red')
CoLR = color_it(font_color='cyan', bg_color='light_red')
WoLR = color_it(font_color='white', bg_color='light_red')
LGyoLR = color_it(font_color='light_grey', bg_color='light_red')
DGyoLR = color_it(font_color='dark_grey', bg_color='light_red')
LRoLR = color_it(font_color='light_red', bg_color='light_red')
LGoLR = color_it(font_color='light_green', bg_color='light_red')
LYoLR = color_it(font_color='light_yellow', bg_color='light_red')
LBoLR = color_it(font_color='light_blue', bg_color='light_red')
LMoLR = color_it(font_color='light_magenta', bg_color='light_red')
LCoLR = color_it(font_color='light_cyan', bg_color='light_red')

#<=====>#

KoLG = color_it(font_color='black', bg_color='light_green')
RoLG = color_it(font_color='red', bg_color='light_green')
GoLG = color_it(font_color='green', bg_color='light_green')
YoLG = color_it(font_color='yellow', bg_color='light_green')
BoLG = color_it(font_color='blue', bg_color='light_green')
MoLG = color_it(font_color='magenta', bg_color='light_green')
CoLG = color_it(font_color='cyan', bg_color='light_green')
WoLG = color_it(font_color='white', bg_color='light_green')
LGyoLG = color_it(font_color='light_grey', bg_color='light_green')
DGyoLG = color_it(font_color='dark_grey', bg_color='light_green')
LRoLG = color_it(font_color='light_red', bg_color='light_green')
LGoLG = color_it(font_color='light_green', bg_color='light_green')
LYoLG = color_it(font_color='light_yellow', bg_color='light_green')
LBoLG = color_it(font_color='light_blue', bg_color='light_green')
LMoLG = color_it(font_color='light_magenta', bg_color='light_green')
LCoLG = color_it(font_color='light_cyan', bg_color='light_green')

#<=====>#

KoLY = color_it(font_color='black', bg_color='light_yellow')
RoLY = color_it(font_color='red', bg_color='light_yellow')
GoLY = color_it(font_color='green', bg_color='light_yellow')
YoLY = color_it(font_color='yellow', bg_color='light_yellow')
BoLY = color_it(font_color='blue', bg_color='light_yellow')
MoLY = color_it(font_color='magenta', bg_color='light_yellow')
CoLY = color_it(font_color='cyan', bg_color='light_yellow')
WoLY = color_it(font_color='white', bg_color='light_yellow')
LGyoLY = color_it(font_color='light_grey', bg_color='light_yellow')
DGyoLY = color_it(font_color='dark_grey', bg_color='light_yellow')
LRoLY = color_it(font_color='light_red', bg_color='light_yellow')
LGoLY = color_it(font_color='light_green', bg_color='light_yellow')
LYoLY = color_it(font_color='light_yellow', bg_color='light_yellow')
LBoLY = color_it(font_color='light_blue', bg_color='light_yellow')
LMoLY = color_it(font_color='light_magenta', bg_color='light_yellow')
LCoLY = color_it(font_color='light_cyan', bg_color='light_yellow')

#<=====>#

KoLB = color_it(font_color='black', bg_color='light_blue')
RoLB = color_it(font_color='red', bg_color='light_blue')
GoLB = color_it(font_color='green', bg_color='light_blue')
YoLB = color_it(font_color='yellow', bg_color='light_blue')
BoLB = color_it(font_color='blue', bg_color='light_blue')
MoLB = color_it(font_color='magenta', bg_color='light_blue')
CoLB = color_it(font_color='cyan', bg_color='light_blue')
WoLB = color_it(font_color='white', bg_color='light_blue')
LGyoLB = color_it(font_color='light_grey', bg_color='light_blue')
DGyoLB = color_it(font_color='dark_grey', bg_color='light_blue')
LRoLB = color_it(font_color='light_red', bg_color='light_blue')
LGoLB = color_it(font_color='light_green', bg_color='light_blue')
LYoLB = color_it(font_color='light_yellow', bg_color='light_blue')
LBoLB = color_it(font_color='light_blue', bg_color='light_blue')
LMoLB = color_it(font_color='light_magenta', bg_color='light_blue')
LCoLB = color_it(font_color='light_cyan', bg_color='light_blue')

#<=====>#

KoLM = color_it(font_color='black', bg_color='light_magenta')
RoLM = color_it(font_color='red', bg_color='light_magenta')
GoLM = color_it(font_color='green', bg_color='light_magenta')
YoLM = color_it(font_color='yellow', bg_color='light_magenta')
BoLM = color_it(font_color='blue', bg_color='light_magenta')
MoLM = color_it(font_color='magenta', bg_color='light_magenta')
CoLM = color_it(font_color='cyan', bg_color='light_magenta')
WoLM = color_it(font_color='white', bg_color='light_magenta')
LGyoLM = color_it(font_color='light_grey', bg_color='light_magenta')
DGyoLM = color_it(font_color='dark_grey', bg_color='light_magenta')
LRoLM = color_it(font_color='light_red', bg_color='light_magenta')
LGoLM = color_it(font_color='light_green', bg_color='light_magenta')
LYoLM = color_it(font_color='light_yellow', bg_color='light_magenta')
LBoLM = color_it(font_color='light_blue', bg_color='light_magenta')
LMoLM = color_it(font_color='light_magenta', bg_color='light_magenta')
LCoLM = color_it(font_color='light_cyan', bg_color='light_magenta')

#<=====>#

KoLC = color_it(font_color='black', bg_color='light_cyan')
RoLC = color_it(font_color='red', bg_color='light_cyan')
GoLC = color_it(font_color='green', bg_color='light_cyan')
YoLC = color_it(font_color='yellow', bg_color='light_cyan')
BoLC = color_it(font_color='blue', bg_color='light_cyan')
MoLC = color_it(font_color='magenta', bg_color='light_cyan')
CoLC = color_it(font_color='cyan', bg_color='light_cyan')
WoLC = color_it(font_color='white', bg_color='light_cyan')
LGyoLC = color_it(font_color='light_grey', bg_color='light_cyan')
DGyoLC = color_it(font_color='dark_grey', bg_color='light_cyan')
LRoLC = color_it(font_color='light_red', bg_color='light_cyan')
LGoLC = color_it(font_color='light_green', bg_color='light_cyan')
LYoLC = color_it(font_color='light_yellow', bg_color='light_cyan')
LBoLC = color_it(font_color='light_blue', bg_color='light_cyan')
LMoLC = color_it(font_color='light_magenta', bg_color='light_cyan')
LCoLC = color_it(font_color='light_cyan', bg_color='light_cyan')

#<=====>#

# Example usage in __main__
if __name__ == '__main__':
    # Example usage of cp
    cp('Hello, World!', font_color='green', bg_color='black', bold=True)
    
    # Example usage of cs
    colored_text = cs('This is colored text.', font_color='blue', bg_color='white', italic=True)
    print(colored_text)
    
    # Run additional demos or examples as needed
    cp('demos','white','green')
    c.demo1()
    c.demo2()
    c.demo3()
    c.demo4()
    c.demo5()
    c.demo6()
    c.demo7()
    c.demo8()
    c.demo9()

#<=====>#


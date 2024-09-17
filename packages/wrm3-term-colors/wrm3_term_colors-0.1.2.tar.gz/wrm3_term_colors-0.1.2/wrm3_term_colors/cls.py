import os
import random
import re
from .pallette import pallette

class CLR:
    str_close = "\033[0m"
    hex_color_pattern = re.compile(r'#[0-9A-Fa-f]{6}\b')

    def __init__(self):
        """
        Initializes the CLR class and checks the terminal environment.
        """
        self.probably_will_work = False
        if os.getenv('WT_SESSION') or (os.getenv('TERM_PROGRAM') == 'vscode'):
            self.probably_will_work = True
        self.pallette = pallette

    def rand_hex(self):
        """Generates a random hex color code."""
        return "#{:02X}{:02X}{:02X}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def name_to_hex(self, color):
        """
        Resolves named colors to their hexadecimal values.
        """
        color = color.lower()
        return pallette.get(color, color)

    def hex_to_int(self, hex_str):
        """Converts a hex string to an integer."""
        return int(hex_str, 16)

    def hex_to_rgb(self, hex_str):
        """Converts a hex color code to an RGB tuple."""
        return tuple(self.hex_to_int(hex_str[i:i+2]) for i in (1, 3, 5))

    def int_to_hex(self, value):
        """Converts an integer to a two-digit hex string."""
        return format(value, '02x')

    def lumi_calc(self, hex_str):
        """Calculates the luminance of a hex color code."""
        r, g, b = self.hex_to_rgb(hex_str)
        return round(0.2126 * r + 0.7152 * g + 0.0722 * b, 2)

    def lumi_get(self, x):
        r = self.hex_to_int(x[1:3])
        g = self.hex_to_int(x[3:5])
        b = self.hex_to_int(x[5:7])
        l = round(0.2126 * r + 0.7152 * g + 0.0722 * b,2)
        return l

    def lumi_inv_hex(self, hex_str):
        """
        Determines an inverse font color based on luminance.
        """
        luminance = self.lumi_calc(hex_str)
        if luminance >= 191:
            return self.name_to_hex('black')
        elif luminance >= 127:
            return self.name_to_hex('red')
        elif luminance >= 63:
            return self.name_to_hex('yellow')
        else:
            return self.name_to_hex('white')

    def inv_hex(self, hex_str):
        """
        Inverts a hex color code.
        """
        r, g, b = self.hex_to_rgb(hex_str)
        inverted = '#{:02X}{:02X}{:02X}'.format(255 - r, 255 - g, 255 - b)
        return inverted

    def color_string(self, text, font_color, bg_color='black', bold=False, italic=False, length=0, align='left'):
        """
        Returns a colorized string using ANSI escape sequences.
        """
        if length:
            length = int(length)
        align_map = {'left': '<', 'center': '^', 'right': '>'}
        align_str = align_map.get(align, '<')
        text = f'{text:{align_str}{max(length, len(text))}}'

        if not self.probably_will_work:
            return text

        font_color = self.name_to_hex(font_color) if not self.hex_color_pattern.match(font_color) else font_color
        bg_color = self.name_to_hex(bg_color) if not self.hex_color_pattern.match(bg_color) else bg_color

        try:
            font_r, font_g, font_b = self.hex_to_rgb(font_color)
            bg_r, bg_g, bg_b = self.hex_to_rgb(bg_color)
        except KeyError:
            return text  # Return plain text if color not found

        style_code = '\x1b[1m' if bold else ''
        style_code += '\x1b[3m' if italic else ''

        ansi_sequence = (
            f"{style_code}"
            f"\x1b[38;2;{font_r};{font_g};{font_b}m"
            f"\x1b[48;2;{bg_r};{bg_g};{bg_b}m"
            f"{text}"
            f"{self.str_close}"
        )
        return ansi_sequence

    def color_print(self, text, font_color, bg_color='black', bold=False, italic=False, length=0, align='left'):
        """
        Prints a colorized string to the terminal.
        """
        colorized_text = self.color_string(text, font_color, bg_color, bold, italic, length, align)
        print(colorized_text)

    def cs(self, text, font_color, bg_color='black', bold=False, italic=False, length=0, align='left'):
        """Alias for color_string."""
        return self.color_string(text, font_color, bg_color, bold, italic, length, align)

    def cp(self, text, font_color, bg_color='black', bold=False, italic=False, length=0, align='left'):
        """Alias for color_print."""
        self.color_print(text, font_color, bg_color, bold, italic, length, align)

    #<=====>#

    def demo1(self):
        pass

    #<=====>#

    def demo2(self):
        print()
        print()
        self.color_print('demo 2', 'white', 'purple', length=200, align='center')
        self.color_print('simple tests...', 'gold', 'mediumvioletred', length=200, align='center')
        print(self.color_string('green print cs test', 'green'))
        self.color_print('green print cp test', 'green')
        self.color_print('Hello World', 'black', 'white', italic=True)
        self.color_print('Yellow On OrangeRed', 'yellow', 'orangered', italic=True)
        self.color_print('#CC3300 On #0033CC', '#CC3300', '#0033CC', italic=True)
        for color in self.pallette:
            color_hex = self.pallette[color]
            r, g, b = self.hex_to_rgb(color_hex)
            lumi = self.lumi_get(color_hex)
            self.cp('{:<35}  {:>8}  {:>3}  {:>3}  {:>3}  {:>6.2f}  {:>3}'.format(color, color_hex, r, g, b, lumi, r+g+b), self.lumi_inv_hex(color_hex), color_hex)

    #<=====>#

    def demo3(self):
        print()
        print()
        self.color_print('demo 3', 'white', 'purple', length=200, align='center')
        self.color_print('random named font color and background colors...', 'gold', 'mediumvioletred', length=200, align='center')
        for i in range(0,25):
            fc = self.rand_hex()
            bgc = self.rand_hex()
            self.color_print(f'{i+1} Random Font Color ({fc}) On A Random Background Color ({bgc})', fc, bgc)

    #<=====>#

    def demo4(self):
        print()
        print()
        self.color_print('demo 4', 'white', 'purple', length=200, align='center')
        self.color_print('loop through the named background colors and use white, yellow, red or black font colors...', 'gold', 'mediumvioletred', length=200, align='center')
        row_str = ''
        cnt = 0
        for color in self.pallette:
            if cnt % 4 == 0:
                print(row_str)
                row_str = ''
            color_score = self.lumi_get(self.pallette[color])
            if color_score >= 191:
                font_color = 'black'
            elif color_score >= 127:
                font_color = 'red'
            elif color_score >= 63:
                font_color = 'yellow'
            else:
                font_color = 'white'
            desc_str = '{} ({}/{})'.format(color, self.pallette[color], self.pallette[font_color])
            prt_str = self.color_string(desc_str, font_color=font_color, bg_color=color, align='center', length=40, italic=True)
            if row_str != '': row_str += ' | '
            row_str += prt_str
            cnt += 1
        print(row_str)

    #<=====>#

    def demo5(self):
        print()
        print()
        self.color_print('demo 5', 'white', 'purple', length=200, align='center')
        self.color_print('loop through the named background colors and calculate an inverted font colors...', 'gold', 'mediumvioletred', length=200, align='center')
        row_str = ''
        cnt = 0
        for color in self.pallette:
            if cnt % 4 == 0:
                print(row_str)
                row_str = ''
            bg_color = self.pallette[color]
            font_color = self.inv_hex(self.pallette[color])
            desc_str = '{} ({}/{})'.format(color, bg_color, font_color)
            prt_str = self.color_string(desc_str, font_color=font_color, bg_color=color, align='center', length=40, italic=True)
            if row_str != '': row_str += ' | '
            row_str += prt_str
            cnt += 1
        print(row_str)

    #<=====>#

    def demo6(self):
        print()
        print()
        self.color_print('demo 6', 'white', 'purple', length=200, align='center')
        self.color_print('loop through the named background colors and and then all named font colors...', 'gold', 'mediumvioletred', length=200, align='center')
        for bg_color in self.pallette:
            row_str = ''
            cnt = 0
            print()
            bg_color_hex = self.name_to_hex(bg_color)
            # bg_lumi = self.lumi_get(bg_color_hex)
            style_color_hex = self.inv_hex(bg_color_hex)
#            style_color_hex = self.lumi_inv_hex(bg_color_hex)
            # style_lumi = self.lumi_get(style_color_hex)
#            print('bg_color_hex : {}, color_hex : {}, bg_lumi : {}, style_lumi : {}'.format(bg_color_hex, style_color_hex, bg_lumi, style_lumi))
            self.cp('{} ({}) Background with {} Font Color'.format(bg_color.upper(), bg_color_hex, style_color_hex), font_color=style_color_hex, bg_color=bg_color_hex, italic=True, length=181, align='center')
            self.cp('-'*181, font_color=bg_color_hex, bg_color=style_color_hex, length=181)
            for font_color in self.pallette:
                if cnt > 0 and cnt % 8 == 0:
                    print(row_str)
                    row_str = ''
                desc_str = '{}'.format(font_color)
                if cnt % 2 == 0:
                    prt_str = self.color_string(desc_str, font_color, bg_color_hex, align='center', length=20, italic=True)
                else:
                    prt_str = self.color_string(desc_str, font_color, bg_color_hex, align='center', length=20)
                div = self.cs(' | ', font_color=bg_color_hex, bg_color=style_color_hex)
                if row_str != '': row_str += div
                row_str += prt_str
                cnt += 1
            print(row_str)

    #<=====>#

    def demo7(self):
        print()
        print()
        self.color_print('demo 7', 'white', 'purple', length=200, align='center')
        self.color_print('loop through some background colors with white & black font colors...', 'gold', 'mediumvioletred', length=200, align='center')
        color_list = ('00','11','22','33','44','55','66','77','88','99','AA','BB','CC','DD','EE','FF')
#        color_list = ('00','33','66','99','CC','FF')
        # pallette = []
        for red_val in color_list:
            for green_val in color_list:
                row_str = ''
                cnt = 0
                for blue_val in color_list:
                    cnt += 1
                    hex_color = f'#{red_val}{green_val}{blue_val}'
                    w = self.cs(text=hex_color, font_color='#FFFFFF', bg_color=hex_color)
                    b = self.cs(text=hex_color, font_color='#000000', bg_color=hex_color)
                    if cnt < len(color_list):
                        wb = '{}{} | '.format(w,b)
                    else:
                        wb = '{}{}'.format(w,b)
                    row_str += wb
                print(row_str)

    #<=====>#

    def demo8(self):
        print()
        print()
        self.color_print('demo 8', 'white', 'purple', length=200, align='center')
        self.color_print('loop through some background colors with calculated inverse font colors...', 'gold', 'mediumvioletred', length=200, align='center')
        color_list = ('00','11','22','33','44','55','66','77','88','99','AA','BB','CC','DD','EE','FF')
        for red_val in color_list:
            for green_val in color_list:
                row_str = ''
                cnt = 0
                for blue_val in color_list:
                    cnt += 1
                    bg_hex_color = f'#{red_val}{green_val}{blue_val}'
                    font_hex_color = self.inv_hex(bg_hex_color)
                    font_hex_color = self.lumi_inv_hex(bg_hex_color)
                    row_str += self.cs(text='{} {}'.format(font_hex_color, bg_hex_color), font_color=font_hex_color, bg_color=bg_hex_color)
                    if cnt < len(color_list): row_str += ' '
                print(row_str)

    #<=====>#

    def demo9(self):
        print()
        print()
        self.color_print('demo 9', 'white', 'purple', length=200, align='center')
        self.color_print('loop through some background colors with calculated inverse font colors...', 'gold', 'mediumvioletred', length=200, align='center')
#        hex_vals = ('0','3','6','9','C','F')
#        hex_vals = ('0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F')
        hex_vals = ('0','2','4','6','8','A','C','E')
        possible_vals = []
        for d1 in hex_vals:
            for d2 in hex_vals:
                hn = '{}{}'.format(d1,d2)
                possible_vals.append(hn)
        row_str = ''
        cnt = 0
        all_cnt = 0
        for red_val in possible_vals:
            for green_val in possible_vals:
                for blue_val in possible_vals:
                    cnt += 1
                    all_cnt += 1
                    bg_hex_color = f'#{red_val}{green_val}{blue_val}'
                    font_hex_color = self.inv_hex(bg_hex_color)
#                    font_hex_color = self.lumi_inv_hex(bg_hex_color)
                    row_str += self.cs(text='{} {}'.format(font_hex_color, bg_hex_color), font_color=font_hex_color, bg_color=bg_hex_color)
                    if cnt < len(hex_vals):
                        row_str += ' '
                    else:
                        print(row_str)
                        row_str = ''
                        cnt = 0
        print('all_cnt : {}'.format(all_cnt))

    #<=====>#


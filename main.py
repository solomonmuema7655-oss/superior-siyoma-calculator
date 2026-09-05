# ============================================================
# SUPERIOR SIYOMA SCIENTIFIC CALCULATOR V2
# ============================================================
# Copyright © 2026 SiyomaCodingPrograms
# ============================================================
#
# FEATURES
# ------------------------------------------------------------
# Basic arithmetic
# Powers and roots
# Factorial
# nPr - Permutations
# nCr - Combinations
# sin, cos, tan
# sin-1, cos-1, tan-1
# sinh, cosh, tanh
# Logarithms
# Natural logarithm
# pi and e
# Percentage
# Absolute value
# Reciprocal
# Sign toggle (+/-)
# DEG / RAD mode
# Memory M+, M-, MR, MC
# Ans function
# Random numbers
# Calculation history
# Error handling
# ============================================================

import math
import random

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView


# ============================================================
# CALCULATOR ENGINE
# ============================================================

class CalculatorEngine:

    def __init__(self):

        self.memory = 0
        self.answer = 0
        self.degrees = True
        self.history = []

    # --------------------------------------------------------
    # PERMUTATION
    # --------------------------------------------------------

    def nPr(self, n, r):

        n = int(n)
        r = int(r)

        if n < 0 or r < 0 or r > n:
            raise ValueError

        return math.factorial(n) // math.factorial(n - r)

    # --------------------------------------------------------
    # COMBINATION
    # --------------------------------------------------------

    def nCr(self, n, r):

        n = int(n)
        r = int(r)

        if n < 0 or r < 0 or r > n:
            raise ValueError

        return (
            math.factorial(n)
            //
            (
                math.factorial(r)
                * math.factorial(n - r)
            )
        )

    # --------------------------------------------------------
    # TRIGONOMETRIC FUNCTIONS
    # --------------------------------------------------------

    def sin(self, x):

        if self.degrees:
            x = math.radians(x)

        return math.sin(x)

    def cos(self, x):

        if self.degrees:
            x = math.radians(x)

        return math.cos(x)

    def tan(self, x):

        if self.degrees:
            x = math.radians(x)

        return math.tan(x)

    # --------------------------------------------------------
    # INVERSE TRIGONOMETRIC FUNCTIONS
    # --------------------------------------------------------

    def asin(self, x):

        result = math.asin(x)

        if self.degrees:
            return math.degrees(result)

        return result

    def acos(self, x):

        result = math.acos(x)

        if self.degrees:
            return math.degrees(result)

        return result

    def atan(self, x):

        result = math.atan(x)

        if self.degrees:
            return math.degrees(result)

        return result

    # --------------------------------------------------------
    # HYPERBOLIC FUNCTIONS
    # --------------------------------------------------------

    def sinh(self, x):
        return math.sinh(x)

    def cosh(self, x):
        return math.cosh(x)

    def tanh(self, x):
        return math.tanh(x)

    # --------------------------------------------------------
    # INVERSE HYPERBOLIC FUNCTIONS
    # --------------------------------------------------------

    def asinh(self, x):
        return math.asinh(x)

    def acosh(self, x):
        return math.acosh(x)

    def atanh(self, x):
        return math.atanh(x)

    # --------------------------------------------------------
    # GENERAL ROOT
    # --------------------------------------------------------

    def root(self, x, n):

        if n == 0:
            raise ValueError

        if x < 0 and n % 2 == 0:
            raise ValueError

        if x < 0:
            return -((-x) ** (1 / n))

        return x ** (1 / n)

    # --------------------------------------------------------
    # MAIN CALCULATION
    # --------------------------------------------------------

    def calculate(self, expression):

        try:

            expression = expression.replace("^", "**")

            allowed = {

                # Constants
                "pi": math.pi,
                "e": math.e,

                # Basic
                "sqrt": math.sqrt,
                "abs": abs,

                # Logarithms
                "log": math.log10,
                "ln": math.log,

                # Factorial
                "factorial": math.factorial,

                # Permutations
                "nPr": self.nPr,

                # Combinations
                "nCr": self.nCr,

                # Trigonometry
                "sin": self.sin,
                "cos": self.cos,
                "tan": self.tan,

                # Inverse trigonometry
                "asin": self.asin,
                "acos": self.acos,
                "atan": self.atan,

                # Hyperbolic
                "sinh": self.sinh,
                "cosh": self.cosh,
                "tanh": self.tanh,

                # Inverse hyperbolic
                "asinh": self.asinh,
                "acosh": self.acosh,
                "atanh": self.atanh,

                # General root
                "root": self.root,

                # Powers
                "pow": pow
            }

            result = eval(
                expression,
                {"__builtins__": {}},
                allowed
            )

            self.answer = result

            self.history.append(
                f"{expression} = {result}"
            )

            return result

        except ZeroDivisionError:
            return "ERROR: Division by zero"

        except ValueError:
            return "ERROR: Invalid value"

        except OverflowError:
            return "ERROR: Number too large"

        except Exception:
            return "ERROR"


# ============================================================
# USER INTERFACE
# ============================================================

class SuperiorCalculator(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(
            orientation="vertical",
            spacing=dp(4),
            padding=dp(7),
            **kwargs
        )

        self.engine = CalculatorEngine()

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title = Label(
            text="[b]SUPERIOR SIYOMA[/b]",
            markup=True,
            font_size=dp(23),
            size_hint_y=None,
            height=dp(40)
        )

        self.add_widget(title)

        subtitle = Label(
            text="SCIENTIFIC - ENGINEERING - STATISTICS",
            font_size=dp(11),
            size_hint_y=None,
            height=dp(23)
        )

        self.add_widget(subtitle)

        # ----------------------------------------------------
        # DISPLAY
        # ----------------------------------------------------
        # readonly=True: display is driven only by button presses,
        # so the on-screen keyboard never pops up and the eval
        # allow-list never sees stray user-typed characters.

        self.display = TextInput(
            multiline=False,
            readonly=True,
            font_size=dp(24),
            halign="right",
            size_hint_y=None,
            height=dp(65)
        )

        self.add_widget(self.display)

        # ----------------------------------------------------
        # MODE / ANSWER
        # ----------------------------------------------------

        info = BoxLayout(
            size_hint_y=None,
            height=dp(35)
        )

        self.mode_button = Button(
            text="DEG"
        )

        self.mode_button.bind(
            on_press=self.toggle_mode
        )

        info.add_widget(self.mode_button)

        self.answer_label = Label(
            text="Ans: 0"
        )

        info.add_widget(self.answer_label)

        self.add_widget(info)

        # ----------------------------------------------------
        # BUTTON GRID
        # ----------------------------------------------------
        # All labels are plain ASCII so nothing renders as a
        # missing-glyph box on devices whose font doesn't cover
        # symbols like √ × ÷ ⌫ π ² ⁻¹ ʸ.

        grid = GridLayout(
            cols=5,
            spacing=dp(3)
        )

        buttons = [

            # Memory
            "MC", "MR", "M+", "M-", "AC",

            # Trigonometry
            "sin", "cos", "tan", "asin", "acos",

            "atan", "sinh", "cosh", "tanh", "sqrt",

            # Advanced mathematics
            "nPr", "nCr", "n!", "x^2", "x^y",

            "root", "1/x", "|x|", "%", "log",

            "ln", "pi", "e", "(", ")",

            # Numbers
            "7", "8", "9", "/", "DEL",

            "4", "5", "6", "*", "^",

            "1", "2", "3", "-", "RAND",

            "0", ".", "=", "+", "Ans",

            # Inverse hyperbolic + sign toggle
            "asinh", "acosh", "atanh", "HISTORY", "+/-"
        ]

        for text in buttons:

            button = Button(
                text=text,
                font_size=dp(14)
            )

            button.bind(
                on_press=self.button_pressed
            )

            grid.add_widget(button)

        self.add_widget(grid)

        # ----------------------------------------------------
        # HISTORY
        # ----------------------------------------------------

        history_title = Label(
            text="[b]CALCULATION HISTORY[/b]",
            markup=True,
            size_hint_y=None,
            height=dp(25)
        )

        self.add_widget(history_title)

        scroll = ScrollView(
            size_hint_y=None,
            height=dp(65)
        )

        self.history_label = Label(
            text="",
            size_hint_y=None,
            halign="left",
            valign="top"
        )

        self.history_label.bind(
            texture_size=self.history_label.setter("size")
        )

        scroll.add_widget(self.history_label)

        self.add_widget(scroll)

        # ----------------------------------------------------
        # COPYRIGHT
        # ----------------------------------------------------

        copyright_label = Label(
            text="(c) 2026 SiyomaCodingPrograms",
            font_size=dp(10),
            size_hint_y=None,
            height=dp(22)
        )

        self.add_widget(copyright_label)

    # ========================================================
    # BUTTON HANDLER
    # ========================================================

    def button_pressed(self, button):

        value = button.text

        # ----------------------------------------------------
        # ALL CLEAR (AC handles both clear and all-clear)
        # ----------------------------------------------------

        if value == "AC":
            self.display.text = ""
            return

        # ----------------------------------------------------
        # BACKSPACE
        # ----------------------------------------------------

        if value == "DEL":
            self.display.text = self.display.text[:-1]
            return

        # ----------------------------------------------------
        # MEMORY CLEAR
        # ----------------------------------------------------

        if value == "MC":
            self.engine.memory = 0
            return

        # ----------------------------------------------------
        # MEMORY RECALL
        # ----------------------------------------------------

        if value == "MR":
            self.display.text += str(self.engine.memory)
            return

        # ----------------------------------------------------
        # MEMORY ADD
        # ----------------------------------------------------

        if value == "M+":

            result = self.engine.calculate(self.display.text)

            if isinstance(result, (int, float)):
                self.engine.memory += result

            return

        # ----------------------------------------------------
        # MEMORY SUBTRACT
        # ----------------------------------------------------

        if value == "M-":

            result = self.engine.calculate(self.display.text)

            if isinstance(result, (int, float)):
                self.engine.memory -= result

            return

        # ----------------------------------------------------
        # ANSWER
        # ----------------------------------------------------

        if value == "Ans":
            self.display.text += str(self.engine.answer)
            return

        # ----------------------------------------------------
        # RANDOM NUMBER
        # ----------------------------------------------------

        if value == "RAND":
            self.display.text += str(random.random())
            return

        # ----------------------------------------------------
        # HISTORY
        # ----------------------------------------------------

        if value == "HISTORY":
            self.update_history()
            return

        # ----------------------------------------------------
        # SIGN TOGGLE
        # ----------------------------------------------------

        if value == "+/-":

            text = self.display.text

            if not text:
                return

            if text.startswith("-("):
                self.display.text = text[2:-1] if text.endswith(")") else text[1:]
            elif text.startswith("-"):
                self.display.text = text[1:]
            else:
                self.display.text = f"-({text})"

            return

        # ----------------------------------------------------
        # FACTORIAL
        # ----------------------------------------------------

        if value == "n!":
            self.display.text += "factorial("
            return

        # ----------------------------------------------------
        # SQUARE ROOT
        # ----------------------------------------------------

        if value == "sqrt":
            self.display.text += "sqrt("
            return

        # ----------------------------------------------------
        # ABSOLUTE VALUE
        # ----------------------------------------------------

        if value == "|x|":
            self.display.text += "abs("
            return

        # ----------------------------------------------------
        # RECIPROCAL
        # ----------------------------------------------------

        if value == "1/x":

            expression = self.display.text
            self.display.text = f"1/({expression})"
            return

        # ----------------------------------------------------
        # SQUARE
        # ----------------------------------------------------

        if value == "x^2":

            expression = self.display.text
            self.display.text = f"({expression})**2"
            return

        # ----------------------------------------------------
        # POWER
        # ----------------------------------------------------

        if value == "x^y":
            self.display.text += "^"
            return

        # ----------------------------------------------------
        # GENERAL ROOT
        # ----------------------------------------------------

        if value == "root":
            self.display.text += "root("
            return

        # ----------------------------------------------------
        # PERCENTAGE
        # ----------------------------------------------------

        if value == "%":
            self.display.text += "/100"
            return

        # ----------------------------------------------------
        # FUNCTIONS
        # ----------------------------------------------------

        functions = [
            "sin", "cos", "tan",
            "asin", "acos", "atan",
            "sinh", "cosh", "tanh",
            "asinh", "acosh", "atanh",
            "log", "ln"
        ]

        if value in functions:
            self.display.text += value + "("
            return

        # ----------------------------------------------------
        # nPr / nCr
        # ----------------------------------------------------

        if value == "nPr":
            self.display.text += "nPr("
            return

        if value == "nCr":
            self.display.text += "nCr("
            return

        # ----------------------------------------------------
        # EQUALS
        # ----------------------------------------------------

        if value == "=":

            expression = self.display.text
            result = self.engine.calculate(expression)

            if isinstance(result, float):

                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)

            self.display.text = str(result)
            self.answer_label.text = f"Ans: {result}"
            self.update_history()

            return

        # ----------------------------------------------------
        # NORMAL BUTTON (digits, ., pi, e, (, ), + - * /)
        # ----------------------------------------------------

        self.display.text += value

    # ========================================================
    # DEG / RAD
    # ========================================================

    def toggle_mode(self, instance):

        self.engine.degrees = not self.engine.degrees

        if self.engine.degrees:
            self.mode_button.text = "DEG"
        else:
            self.mode_button.text = "RAD"

    # ========================================================
    # HISTORY
    # ========================================================

    def update_history(self):
        self.history_label.text = "\n".join(self.engine.history[-10:])


# ============================================================
# APPLICATION
# ============================================================

class SuperiorCalculatorApp(App):

    def build(self):

        Window.clearcolor = (0.04, 0.04, 0.04, 1)
        return SuperiorCalculator()


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    SuperiorCalculatorApp().run()

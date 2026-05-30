from __future__ import annotations
from abc import ABC, abstractmethod
from BigBigfloat import Bigfloat

'''
string ::= <number> <number> <number>
number ::= [<sign>] <mantissa> [<exp>] | <special>
sign   ::= "+" | "-"
mantissa ::= <digits> [<point> <digits>]
point  ::= "." | ","
digits ::= <digit> | <digit> {<digit> | "_"}
digit  ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
exp    ::= "e" | "E", [<sign>], <digit>+
special ::= "inf" | "infinity" | "nan"
'''

VALUE_ERROR = "некорректный ввод"


def find_point(text: str) -> int:
    for ch in (".", ","):
        if ch in text:
            return text.index(ch)
    return -1


def find_exp(text: str) -> int:
    for ch in ("e", "E"):
        if ch in text:
            return text.index(ch)
    return -1


def strip_underscores(text: str) -> str:
    if "_" not in text:
        return text
    out = []
    for i, ch in enumerate(text):
        if ch == "_":
            if i == 0 or i == len(text) - 1:
                raise ValueError(VALUE_ERROR)
            if not text[i - 1].isdigit() or not text[i + 1].isdigit():
                raise ValueError(VALUE_ERROR)
            continue
        out.append(ch)
    return "".join(out)


class Interpret(ABC):


    @abstractmethod
    def interpret(self):
        pass


class Context:

    def __init__(self):
        self.__a = Bigfloat()
        self.__b = Bigfloat()
        self.__c = Bigfloat()
    
    def get_a(self):
        return self.__a
    
    def get_b(self):
        return self.__b
    
    def get_c(self):
        return self.__c
    
    def set_a(self,
              number: Bigfloat):
        
        self.__a = number

    def set_b(self,
              number: Bigfloat):
        
        self.__b = number

    def set_c(self,
              number: Bigfloat):
        
        self.__c = number



class String(Interpret):

    def __init__(self,
                 string: str,
                 context: Context):
        
        self.string = string
        self.context = context
        self.interpret()

    def interpret(self) -> None:
        
        numbers = self.string.split()
        if len(numbers) != 3:
            raise ValueError(VALUE_ERROR)
        self.context.set_a(Number(numbers[0]).interpret())
        self.context.set_b(Number(numbers[1]).interpret())
        self.context.set_c(Number(numbers[2]).interpret())

    
class Number(Interpret):

    INF_NAMES = {"inf", "infinity"}
    NAN_NAMES = {"nan"}

    def __init__(self,
                 number: str):
        
        self.number = number.strip()
    
    def interpret(self) -> Bigfloat:
        if not self.number:
            raise ValueError(VALUE_ERROR)

        negative = Sign(self.number).interpret()

        core = self.number
        if core and core[0] in "+-":
            core = core[1:]
        if core and core[0] in "+-":
            raise ValueError(VALUE_ERROR)

        core_lower = core.lower()
        if core_lower in self.INF_NAMES:
            return Bigfloat.make_inf(negative)
        if core_lower in self.NAN_NAMES:
            return Bigfloat.make_nan()

        core = strip_underscores(core)

        mant, exp_part = self.split_exp(core)

        self.check_leading_zeros(mant)

        exp = Exponent(exp_part).interpret()
        dot = Point(mant).interpret()

        mant = self.remove_point(mant)
        if mant == "":
            raise ValueError(VALUE_ERROR)

        if Zero(mant).interpret():
            return Bigfloat.make_Bigfloat_from_int(0)

        mant = mant.lstrip("0")

        number = Bigfloat()
        number.negative = negative
        number.number = Digits(mant).interpret()
        number.exp = exp + dot
        return number

    def split_exp(self, text: str):
        idx = find_exp(text)
        if idx == -1:
            return text, None

        mant = text[:idx]
        exp = text[idx + 1:]

        if not exp:
            raise ValueError(VALUE_ERROR)

        return mant, exp

    def check_leading_zeros(self, text: str):
        idx = find_point(text)
        left = text if idx == -1 else text[:idx]
        if len(left) > 1 and left.startswith("0"):
            raise ValueError(VALUE_ERROR)

    def remove_point(self, text: str):
        idx = find_point(text)
        if idx == -1:
            return text
        rest = text[idx + 1:]
        if find_point(rest) != -1:
            raise ValueError(VALUE_ERROR)
        return text[:idx] + text[idx + 1:]


class Zero(Interpret):

    def __init__(self,
                 number: str):
        
        self.number = number
        
    def interpret(self):
        if self.number == "0.0" or self.number == "0" or self.number == "0,0":
            return True
        return all(ch == "0" for ch in self.number)


class Sign(Interpret):

    def __init__(self,
                 number: str):
        
        self.number = number

    def interpret(self):
        if self.number and self.number[0] == "-":
            return True
        return False
        

class Digits(Interpret):

    def __init__(self,
                 number: str):
        
        self.number = number

    def interpret(self) -> list[int]:
        self.number = self.number.replace(".", "", 1)
        self.number = self.number.replace(",", "", 1)
        if self.number and (self.number[0] == "-" or self.number[0] == "+"):
            self.number = self.number[1:]
        result = []
        len_number = len(self.number)
        for i in range(len_number, 0, -Bigfloat.BASE):
            start_pos = max(0, i - Bigfloat.BASE)
            digit = self.number[start_pos:i]
            digit = Digit(digit).interpret()
            result.append(digit)
        return result
        
class Digit(Interpret):

    def __init__(self,
                 digit: str):
        self.digit = digit

    def interpret(self):

        try:
            self.digit = int(self.digit)
            return self.digit
        except:
            raise ValueError(VALUE_ERROR)

   

class Point(Interpret):

    def __init__(self,
                 number: str):
        
        self.number = number

    def interpret(self):
        pos_point = find_point(self.number)
        len_number = len(self.number)
        if pos_point != -1:
            exp = -(len_number - (pos_point + 1))
        else:
            return 0
        return exp


class Exponent(Interpret):

    def __init__(self,
                 text):
        self.text = text

    def interpret(self):
        if self.text is None:
            return 0
        sign = 1
        text = self.text
        if text and text[0] in "+-":
            sign = -1 if text[0] == "-" else 1
            text = text[1:]
        if not text or not text.isdigit():
            raise ValueError(VALUE_ERROR)

        return sign * int(text)



if __name__ == "__main__":
    context = Context()
    string = input()
    STRING = String(string, context)
    a = STRING.context.get_a()
    b = STRING.context.get_b()
    c = STRING.context.get_c()
    print(a.number, a.exp, a.negative)
    print(b.number, b.exp, b.negative)
    print(c.number, c.exp, c.negative)

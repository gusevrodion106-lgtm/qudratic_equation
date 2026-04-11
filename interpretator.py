from __future__ import annotations
from abc import ABC, abstractmethod
from BigBigfloat import Bigfloat



VALUE_ERROR = "некорректный ввод"

'''
string ::= <number> <number> <number>
number ::= [<sign>] <digits> <point> <digits> | [<sign>] <digits> | <zero>
sign ::= [+ | -]
digits ::= <digit>+
zero ::= "0.0" | "0"
point ::= "."
digit ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

'''


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

    def __init__(self,
                 number: str):
        
        self.number = number
    
    def interpret(self) -> Bigfloat:
        if Zero(self.number).interpret() == True:
            return Bigfloat.make_Bigfloat_from_int(0)
        number = Bigfloat()
        number.negative = Sign(self.number).interpret()
        number.number = Digits(self.number).interpret()
        number.exp = Point(self.number).interpret()
        return number


class Zero(Interpret):

    def __init__(self,
                 number: str):
        
        self.number = number
        
    def interpret(self):
        if self.number == "0.0" or self.number == "0":
            return True
        return False


class Sign(Interpret):

    def __init__(self,
                 number: str):
        
        self.number = number

    def interpret(self):
        if self.number[0] == "-":
            return True
        return False
        

class Digits(Interpret):

    def __init__(self,
                 number: str):
        
        self.number = number

    def interpret(self) -> list[int]:
        self.number = self.number.replace(".", "", 1)
        if self.number[0] == "-" or self.number[0] == "+":
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
        pos_point = self.number.find(".")
        len_number = len(self.number)
        if pos_point != -1:
            exp = -(len_number - (pos_point + 1))
        else:
            return 0
        return exp



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
    

        

        
        

        


        


        
            
        

        


        










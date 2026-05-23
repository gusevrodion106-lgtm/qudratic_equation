from __future__ import annotations
from interpretator import Context, String, Number
from BigBigfloat import Bigfloat
from typing import Any
from time import *
import math


class Messages:

    EQUATION_HAS_ONLY_ONE_ROOT = "уравнение имеет только один корень" 
    EQUATION_HAS_TWO_SAME_ROOTS = "уравнение имеет 2 совпадающих корня" 
    COMPLEX_ROOTS = "уравнение имеет только комплексные решения"
    NO_ROOTS = "нет решений"
    INFINITE_ROOTS = "бесконечное число решений"

    information_messages = [EQUATION_HAS_ONLY_ONE_ROOT, EQUATION_HAS_TWO_SAME_ROOTS, COMPLEX_ROOTS]
    important_messages = [NO_ROOTS, INFINITE_ROOTS]
    


class Data:

    def __init__(self,
                 string: str):

        context = Context()
        STRING = String(string, context)
        self.__a = STRING.context.get_a()
        self.__b = STRING.context.get_b()
        self.__c = STRING.context.get_c()

    def get_a(self):
        return self.__a
    
    def get_b(self):
        return self.__b
    
    def get_c(self):
        return self.__c
    

class Answer:

    def __init__(self,
                 x1: Bigfloat = Bigfloat(),
                 x2: Bigfloat = Bigfloat(),
                 message: Messages = None):
        
        self.__x1 = x1
        self.__x2 = x2
        self.__message = message

    def get_x1(self) -> Bigfloat:
        return self.__x1
    
    def get_x2(self) -> Bigfloat:
        return self.__x2
    
    def get_message(self) -> Bigfloat:
        return self.__message
    
    def set_x1(self,
               x1: Bigfloat) -> None:
        self.__x1 = x1

    def set_x2(self,
               x2: Bigfloat) -> None:
        self.__x2 = x2

    def set_message(self,
                    message: Messages) -> None:
        self.__message = message


class complex_Answer:

    def __init__(self,
                 x1: tuple,
                 x2: tuple,
                 message: Messages = None):
        
        self.__real_part_x1 = x1[0]
        self.__image_part_x1 = x1[1]
        self.__real_part_x2 = x2[0]
        self.__image_part_x2 = x2[1]
        self.__message = message

        
    def get_x1(self) -> str:
        return "{0} + {1}i".format(self.__real_part_x1, self.__image_part_x1)
    
    def get_x2(self) -> str:
        return "{0} - {1}i".format(self.__real_part_x2, self.__image_part_x2)
    
    def get_message(self) -> Bigfloat:
        return self.__message
    
    def set_message(self,
                    message: Messages) -> None:
        self.__message = message

    


def calculate_discriminant(a: Bigfloat,
                           b: Bigfloat,
                           c: Bigfloat) -> Bigfloat:
    
    if c._is_zero():
        return b * b
    four = Bigfloat.make_Bigfloat_from_int(4)
    return b * b - four * a * c


def calculate_x1(  sqrt_d: Bigfloat,
                      one_divide_by_two_a: Bigfloat,
                      b: Bigfloat) -> Bigfloat:

    return (b + sqrt_d) * one_divide_by_two_a


def calculate_x2(sqrt_d: Bigfloat,
                      one_divide_by_two_a: Bigfloat,
                      b: Bigfloat) -> Bigfloat:
    
    return (b - sqrt_d) * one_divide_by_two_a


def calculate_complex_x1(sqrt_d: Bigfloat,
                         one_divide_by_two_a: Bigfloat,
                         b: Bigfloat) -> tuple:
    
    real_part = b * one_divide_by_two_a
    image_part = sqrt_d * one_divide_by_two_a
    return real_part, image_part


def calculate_complex_x2(sqrt_d: Bigfloat,
                         one_divide_by_two_a: Bigfloat,
                         b: Bigfloat) -> tuple:
    
    real_part = b * one_divide_by_two_a
    image_part = sqrt_d * one_divide_by_two_a
    return real_part, image_part

  

def calculate_answer_with_positive_discriminant(d: Bigfloat, 
                                                one_divide_by_two_a: Bigfloat, 
                                                b: Bigfloat) -> Answer:
    
    
    b.reverse_sign()
    if d == 0:
        answer = Answer(calculate_x1(Bigfloat.make_Bigfloat_from_int(0), one_divide_by_two_a, b))
        answer.set_message(Messages.EQUATION_HAS_TWO_SAME_ROOTS)
    else:
        sqrt_d = Bigfloat.sqrt(d)
        answer = Answer(calculate_x1(sqrt_d, one_divide_by_two_a, b), calculate_x2(sqrt_d, one_divide_by_two_a, b))
    return answer
    

def calculate_answer_of_linear_equation(b: Bigfloat,
                                        c: Bigfloat) -> Answer:
    
    answer = Answer()
    if b == 0:
        if c == 0:
            answer.set_message(Messages.INFINITE_ROOTS)
            return answer
        else:
            answer.set_message(Messages.NO_ROOTS)
            return answer
    else:
        c.reverse_sign()
        answer.set_message(Messages.EQUATION_HAS_ONLY_ONE_ROOT)
        answer.set_x1(c / b)
        return answer

    
def calculate_answer_with_negative_discriminant(d: Bigfloat, 
                                                one_divide_by_two_a: Bigfloat, 
                                                b: Bigfloat) -> complex_Answer:
    
    d.reverse_sign()
    sqrt_d = Bigfloat.sqrt(d)
    b.reverse_sign()
    answer = complex_Answer(calculate_complex_x1(sqrt_d, one_divide_by_two_a, b), calculate_complex_x2(sqrt_d, one_divide_by_two_a, b))
    answer.set_message(Messages.COMPLEX_ROOTS)
    return answer



def has_special(data: Data) -> bool:
    return any(not x.is_finite() for x in (data.get_a(), data.get_b(), data.get_c()))


def bf_to_float(bf: Bigfloat) -> float:
    if bf.is_nan():
        return math.nan
    if bf.is_inf():
        return -math.inf if bf.negative else math.inf
    s = str(bf).strip().lower()
    if 'e' in s:
        base, exp = s.split('e')
        if int(exp) > 308:
            return math.inf if not bf.negative else -math.inf
    if not s or s in {'.', '+', '-'}:
        return math.nan
    return float(s)


def float_to_bf(x: float) -> Bigfloat:
    if math.isnan(x):
        return Bigfloat.make_nan()
    if math.isinf(x):
        return Bigfloat.make_inf(x < 0)
    return Number(repr(x)).interpret()


def special_solve(data: Data) -> Answer | complex_Answer:
    a = bf_to_float(data.get_a())
    b = bf_to_float(data.get_b())
    c = bf_to_float(data.get_c())

    if math.isnan(a) or math.isnan(b) or math.isnan(c):
        nan = Bigfloat.make_nan()
        answer = Answer(nan, nan)
        return answer

    if a == 0.0:
        if b == 0.0:
            if c == 0.0:
                answer = Answer()
                answer.set_message(Messages.INFINITE_ROOTS)
                return answer
            if math.isinf(c):
                answer = Answer(Bigfloat.make_nan())
                answer.set_message(Messages.EQUATION_HAS_ONLY_ONE_ROOT)
                return answer
            answer = Answer()
            answer.set_message(Messages.NO_ROOTS)
            return answer
        if math.isinf(b) or math.isinf(c):
            answer = Answer(Bigfloat.make_nan())
            answer.set_message(Messages.EQUATION_HAS_ONLY_ONE_ROOT)
            return answer
        x = -c / b
        if math.isnan(x) or math.isinf(x):
            answer = Answer(Bigfloat.make_nan())
            answer.set_message(Messages.EQUATION_HAS_ONLY_ONE_ROOT)
            return answer
        answer = Answer(float_to_bf(x))
        answer.set_message(Messages.EQUATION_HAS_ONLY_ONE_ROOT)
        return answer

    d = b * b - 4 * a * c
    if math.isnan(d):
        nan = Bigfloat.make_nan()
        answer = Answer(nan, nan)
        return answer

    if d < 0:
        re = -b / (2 * a)
        im = math.sqrt(-d) / (2 * a)
        answer = complex_Answer(
            (float_to_bf(re), float_to_bf(im)),
            (float_to_bf(re), float_to_bf(-im))
        )
        answer.set_message(Messages.COMPLEX_ROOTS)
        return answer

    sqrt_d = math.sqrt(d)
    x1 = (-b + sqrt_d) / (2 * a)
    x2 = (-b - sqrt_d) / (2 * a)
    return Answer(float_to_bf(x1), float_to_bf(x2))


def solve(data: Data) -> Answer:
    if has_special(data):
        return special_solve(data)
    a = data.get_a()
    b = data.get_b()
    c = data.get_c()
    if a == 0:  
        answer = calculate_answer_of_linear_equation(b, c)
        return answer
    d = calculate_discriminant(a, b, c)
    one_divide_by_two_a = (a * Bigfloat.make_Bigfloat_from_int(2)).Newton_method()
    if d >= 0:
        answer = calculate_answer_with_positive_discriminant(d, one_divide_by_two_a, b)
    else:
        answer = calculate_answer_with_negative_discriminant(d, one_divide_by_two_a, b)
    return answer


def output(answer: Any) -> None:

    message = answer.get_message()
    if message in Messages.important_messages:
        print(message)
    else:
        x1 = answer.get_x1()
        x2 = answer.get_x2()
        if message == Messages.EQUATION_HAS_ONLY_ONE_ROOT:
            print(message)
            print("x1 = {0}".format(x1))
        elif message == Messages.EQUATION_HAS_TWO_SAME_ROOTS:
            print(message)
            print("x1 = {0}".format(x1))
        elif message == None:
            print("x1 = {0}".format(x1))
            print("x2 = {0}".format(x2))
        else:
            print(message)
            print("x1 = {0}".format(x1))
            print("x2 = {0}".format(x2))



if __name__ == "__main__":
    data = Data("3" * 10000 + " " + "3" * 10000 + " " + "3" * 10000)
    time1 = time()
    answer = solve(data)
    tim2 = time()
    output(answer)
    print(tim2 - time1)

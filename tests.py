import unittest
from BigBigfloat import Bigfloat
from random import *
from time import *
from decimal import Decimal, getcontext
from math import sqrt
from copy import deepcopy
from квадратка import Data, solve, Messages, Answer
getcontext().prec = 100000




class SupportFunctions:

    def generate_random_int(self,
                               start: int,
                               end: int,
                               sign = 2) -> int:
        
        a = randint(start, end)
        if sign == 2:
            sign = choice([-1, 1])
        elif sign == 1:
            sign = -1
        else:
            sign = 1
        a *= sign
        return a
    
    
    def generate_random_decimal(self) -> Decimal:

        power_exp = randint(-10000, 10000)
        exp = Decimal(10) ** power_exp
        if power_exp > 0:
            digit = self.generate_random_int(1, 10**(10000 - power_exp))
        else:
            digit = self.generate_random_int(1, 10**(10000)) 
        Decimal_digit = Decimal(digit) * exp
        return Decimal_digit


    def make_decimal_from_Bigfloat(self,
                                   digit: Bigfloat) -> Decimal:
        
        str_digit = ""
        for x in reversed(digit.number):
            str_digit += str(x).zfill(digit.BASE)
        if digit.exp >= 0:
            str_digit += "0" * digit.exp
            dec_digit = Decimal(str_digit)
        else:
            if len(str_digit) <= abs(digit.exp):
                dec_digit = Decimal("0." + "0" * (abs(digit.exp) - len(str_digit)) + str_digit)
            else:
                point = len(str_digit) - abs(digit.exp)
                str_digit = str_digit[:point] + "." + str_digit[point:]
                dec_digit = Decimal(str_digit)
        if digit.negative:
            dec_digit *= (-1)
        return dec_digit
    

    def make_int_from_Bigfloat(self,
                               digit: Bigfloat) -> int:
        
        str_digit = ""
        for x in reversed(digit.number):
            str_digit += str(x).zfill(digit.BASE)
        str_digit += "0" * digit.exp
        int_digit = int(str_digit)
        if digit.negative:
            int_digit *= (-1)
        return int_digit
    

    def make_decimal_from_int_with_specified_exp(self,
                                                 digit: int,
                                                 exp: int) -> Decimal:
        
        number = Decimal(digit) 
        power_exp = Decimal(10) ** Decimal(exp)
        number *= power_exp
        return number
    

    def calculate_len_digit(self,
                            digit: int) -> int:
        
        if digit >= 0:
            return len(str(digit))
        else:
            return len(str(digit)) - 1
        
    def generate_random_Bigfloat(self,
                                 From = 1,
                                 To = 10 ** 10000,
                                 sign = 2) -> Bigfloat:

        a = self.generate_random_int(From, To, sign)
        len_a = self.calculate_len_digit(a)
        exp = randint(-10000, 10000)
        if exp + len_a >= 10000:
            exp = 10000 - len_a
        Bigfloat_a = Bigfloat.make_Bigfloat_from_int(a)
        Bigfloat_a.exp = exp
        return Bigfloat_a


    def check_conversion_from_Bigfloat_to_int(self,
                                              digit: int):
        
        Bigfloat_digit = Bigfloat.make_Bigfloat_from_int(digit)
        test_digit = self.make_int_from_Bigfloat(Bigfloat_digit)
        self.assertEqual(test_digit, digit)




# class TestBigfloat(unittest.TestCase, SupportFunctions):

#     COUNT_TESTS = 1

#     def setUp(self):
#         self.bigfloat = Bigfloat()
    
#     def test_make_Bigfloat_from_int_from_1_to_10_power_10(self):

#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_int(1, 10**10)
#             self.check_conversion_from_Bigfloat_to_int(a)

#     def test_make_Bigfloat_from_int_from_10_power_10_to_10_power_100(self):

#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_int(10**10, 10**100)
#             self.check_conversion_from_Bigfloat_to_int(a)

#     def test_make_Bigfloat_from_int_from_10_power_100_to_10_power_1000(self):

#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_int(10**100, 10**1000)
#             self.check_conversion_from_Bigfloat_to_int(a)

#     def test_make_Bigfloat_from_int_from_10_power_1000_to_10_power_10000(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_int(10**1000, 10**10000)
#             self.check_conversion_from_Bigfloat_to_int(a)


#     def test_is_zero_if_number_is_zero(self):
#         for i in range(self.COUNT_TESTS):
#             zero = Bigfloat([0])
#             zero.negative = choice([False, True])
#             assert zero._is_zero() == True

#     def test_is_zero_if_number_is_not_zero(self):
#         for i in range(self.COUNT_TESTS):
#             number = self.generate_random_Bigfloat()
#             if number.number != [0]:
#                 assert number._is_zero() == False
#             else:
#                 assert number._is_zero() == True


#     def test_more_abs_from_1_to_10_power_10(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_int(1, 10**10)
#             b = self.generate_random_int(1, 10**10)
#             Bigfloat_a = Bigfloat.make_Bigfloat_from_int(a)
#             Bigfloat_b = Bigfloat.make_Bigfloat_from_int(b)
#             true_answer = abs(a) > abs(b)
#             test_answer = Bigfloat_a._more_abs(Bigfloat_b)
#             self.assertEqual(test_answer, true_answer)

#     def test_more_abs_from_10_power_10_to_10_power_100(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_int(10**10, 10**100)
#             b = self.generate_random_int(10**10, 10**100)
#             Bigfloat_a = Bigfloat.make_Bigfloat_from_int(a)
#             Bigfloat_b = Bigfloat.make_Bigfloat_from_int(b)
#             true_answer = abs(a) > abs(b)
#             test_answer = Bigfloat_a._more_abs(Bigfloat_b)
#             self.assertEqual(test_answer, true_answer)


#     def test_more_abs_from_10_power_100_to_10_power_1000(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_int(10**100, 10**1000)
#             b = self.generate_random_int(10**100, 10**1000)
#             Bigfloat_a = Bigfloat.make_Bigfloat_from_int(a)
#             Bigfloat_b = Bigfloat.make_Bigfloat_from_int(b)
#             true_answer = abs(a) > abs(b)
#             test_answer = Bigfloat_a._more_abs(Bigfloat_b)
#             self.assertEqual(test_answer, true_answer)

#     def test_more_abs_from_10_power_1000_to_10_power_10000(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_int(10**1000, 10**10000)
#             b = self.generate_random_int(10**1000, 10**10000)
#             Bigfloat_a = Bigfloat.make_Bigfloat_from_int(a)
#             Bigfloat_b = Bigfloat.make_Bigfloat_from_int(b)
#             true_answer = abs(a) > abs(b)
#             test_answer = Bigfloat_a._more_abs(Bigfloat_b)
#             self.assertEqual(test_answer, true_answer)

#     def test_more_abs_with_different_exp(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_int(1, 10**10000)
#             b = self.generate_random_int(1, 10**10000)
#             Bigfloat_a = Bigfloat.make_Bigfloat_from_int(a)
#             Bigfloat_b = Bigfloat.make_Bigfloat_from_int(b)
#             exp_a = randint(-10000, 10000)
#             exp_b = randint(-10000, 10000)
#             Bigfloat_a.exp = exp_a
#             Bigfloat_b.exp = exp_b
#             a = self.make_decimal_from_int_with_specified_exp(a, exp_a)
#             b = self.make_decimal_from_int_with_specified_exp(b, exp_b)
#             true_answer = abs(a) > abs(b)
#             test_answer = Bigfloat_a._more_abs(Bigfloat_b)
#             assert test_answer == true_answer

#     def test_division_exp_by_BASE_after_function_make_exp_multiple_BASE(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_int(1, 10**10000)
#             Bigfloat_a = Bigfloat.make_Bigfloat_from_int(a)
#             exp_a = randint(-10000, 10000)
#             Bigfloat_a.exp = exp_a
#             Bigfloat_a._make_exp_multiple_BASE()
#             assert Bigfloat_a.exp % Bigfloat.BASE == 0

#     def test_sub(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat()
#             b = self.generate_random_Bigfloat()
#             true_a = self.make_decimal_from_Bigfloat(a)
#             true_b = self.make_decimal_from_Bigfloat(b)
#             true_answer = true_a - true_b
#             test_answer = self.make_decimal_from_Bigfloat(a - b)
#             assert true_answer == test_answer

#     def test_sub_with_same_elements(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat()
#             true_answer = Bigfloat([0])
#             test_answer = a - a
#             assert true_answer == test_answer

#     def test_sub_with_zero(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat()
#             zero = Bigfloat([0])
#             test_answer = a - zero
#             assert a == test_answer


#     def test_add(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat()
#             b = self.generate_random_Bigfloat()
#             true_a = self.make_decimal_from_Bigfloat(a)
#             true_b = self.make_decimal_from_Bigfloat(b)
#             true_answer = true_a + true_b
#             test_answer = self.make_decimal_from_Bigfloat(a + b)
#             assert true_answer == test_answer

#     def test_add_with_zero(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat()
#             zero = Bigfloat([0])
#             test_answer = a + zero
#             assert a == test_answer

#     def test_mul_with_same_exp(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_int(1, 10**10000)
#             b = self.generate_random_int(1, 10**10000)
#             true_answer = a * b
#             Bigfloat_a = Bigfloat.make_Bigfloat_from_int(a)
#             Bigfloat_b = Bigfloat.make_Bigfloat_from_int(b)
#             test_answer = Bigfloat_a * Bigfloat_b
#             test_answer = self.make_int_from_Bigfloat(test_answer)
#             assert true_answer == test_answer

#     def test_mul_by_zero(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat()
#             zero = Bigfloat([0])
#             test_answer = a * zero
#             assert test_answer._is_zero()

#     def test_mul_with_different_exp(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat()
#             b = self.generate_random_Bigfloat()
#             true_a = self.make_decimal_from_Bigfloat(a)
#             true_b = self.make_decimal_from_Bigfloat(b)
#             true_answer = true_a * true_b
#             test_answer = a * b
#             test_answer = self.make_decimal_from_Bigfloat(test_answer)
#             assert test_answer == true_answer

#     def test_mul_with_different_sign1(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat()
#             b = self.generate_random_Bigfloat()
#             a.negative = False
#             b.negative = True
#             test_answer = a * b
#             assert test_answer.negative == True

#     def test_mul_with_different_sign2(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat()
#             b = self.generate_random_Bigfloat()
#             a.negative = True
#             b.negative = False
#             test_answer = a * b
#             assert test_answer.negative == True

#     def test_mul_with_same_sign1(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat()
#             b = self.generate_random_Bigfloat()
#             a.negative = False
#             b.negative = False
#             test_answer = a * b
#             assert test_answer.negative == False

#     def test_mul_with_same_sign2(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat()
#             b = self.generate_random_Bigfloat()
#             a.negative = True
#             b.negative = True
#             test_answer = a * b
#             assert test_answer.negative == False

#     def test_division_by_two(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat(From=10, To=10**10)
#             true_a = self.make_decimal_from_Bigfloat(a)
#             true_answer = true_a / Decimal(2)
#             a.divide_by_two()
#             test_answer = self.make_decimal_from_Bigfloat(a)
#             assert true_answer == test_answer, print(a.number, true_answer, "\n", test_answer)


#     def test_division_with_same_exp(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_int(1, 10**10000)
#             b = self.generate_random_int(1, 10**10000)
#             Bigfloat_a = Bigfloat.make_Bigfloat_from_int(a)
#             Bigfloat_b = Bigfloat.make_Bigfloat_from_int(b)
#             true_answer = str(Decimal(a) / Decimal(b))
#             test_answer = Bigfloat_a / Bigfloat_b
#             test_answer = str(self.make_decimal_from_Bigfloat(test_answer))
#             assert true_answer[:10000] == test_answer[:len(true_answer[:10000])]

#     def test_division_with_different_exp(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat()
#             b = self.generate_random_Bigfloat()
#             true_a = self.make_decimal_from_Bigfloat(a)
#             true_b = self.make_decimal_from_Bigfloat(b)
#             true_answer = str(true_a / true_b)
#             test_answer = a / b
#             test_answer = str(self.make_decimal_from_Bigfloat(test_answer))
#             assert true_answer[:10000] == test_answer[:len(true_answer[:10000])]

#     def test_division_by_itself(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat()
#             true_answer = Bigfloat([1])
#             test_answer = a / a
#             assert true_answer == test_answer

#     def test_sqrt(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat(sign=0)
#             true_a = self.make_decimal_from_Bigfloat(a)
#             true_sqrt = str(true_a.sqrt())
#             test_sqrt = Bigfloat.sqrt(a)
#             test_sqrt = str(self.make_decimal_from_Bigfloat(test_sqrt))
#             assert true_sqrt[:10000] == test_sqrt[:10000]

#     def test_sqrt_with_null_exp(self):
#         for i in range(self.COUNT_TESTS):
#             int_a = self.generate_random_int(start=1, end=10**10, sign=0)
#             Bigfloat_a = Bigfloat.make_Bigfloat_from_int(int_a)
#             true_sqrt = str(Decimal(int_a).sqrt())
#             test_sqrt = Bigfloat.sqrt(Bigfloat_a)
#             test_sqrt = str(self.make_decimal_from_Bigfloat(test_sqrt))
#             assert true_sqrt[:10000] == test_sqrt[:10000]

#     def test_sqrt_with_null_exp2(self):
#         for i in range(self.COUNT_TESTS):
#             int_a = self.generate_random_int(start=10**10, end=10**100, sign=0)
#             Bigfloat_a = Bigfloat.make_Bigfloat_from_int(int_a)
#             true_sqrt = str(Decimal(int_a).sqrt())
#             test_sqrt = Bigfloat.sqrt(Bigfloat_a)
#             test_sqrt = str(self.make_decimal_from_Bigfloat(test_sqrt))
#             assert true_sqrt[:10000] == test_sqrt[:10000]

#     def test_sqrt_with_null_exp3(self):
#         for i in range(self.COUNT_TESTS):
#             int_a = self.generate_random_int(start=10**100, end=10**1000, sign=0)
#             Bigfloat_a = Bigfloat.make_Bigfloat_from_int(int_a)
#             true_sqrt = str(Decimal(int_a).sqrt())
#             test_sqrt = Bigfloat.sqrt(Bigfloat_a)
#             test_sqrt = str(self.make_decimal_from_Bigfloat(test_sqrt))
#             assert true_sqrt[:10000] == test_sqrt[:10000]

#     def test_sqrt_with_null_exp4(self):
#         for i in range(self.COUNT_TESTS):
#             int_a = self.generate_random_int(start=10**1000, end=10**10000, sign=0)
#             Bigfloat_a = Bigfloat.make_Bigfloat_from_int(int_a)
#             true_sqrt = str(Decimal(int_a).sqrt())
#             test_sqrt = Bigfloat.sqrt(Bigfloat_a)
#             test_sqrt = str(self.make_decimal_from_Bigfloat(test_sqrt))
#             assert true_sqrt[:10000] == test_sqrt[:10000]

#     def test_sqrt_from_1_to_10_power_10(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat(From=1, To=10**10, sign=0)
#             true_a = self.make_decimal_from_Bigfloat(a)
#             true_sqrt = str(true_a.sqrt())
#             test_sqrt = Bigfloat.sqrt(a)
#             test_sqrt = str(self.make_decimal_from_Bigfloat(test_sqrt))
#             assert true_sqrt[:10000] == test_sqrt[:10000]

#     def test_sqrt_from_10_power_10_to_10_power_100(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat(From=10**10, To=10**100, sign=0)
#             true_a = self.make_decimal_from_Bigfloat(a)
#             true_sqrt = str(true_a.sqrt())
#             test_sqrt = Bigfloat.sqrt(a)
#             test_sqrt = str(self.make_decimal_from_Bigfloat(test_sqrt))
#             assert true_sqrt[:10000] == test_sqrt[:10000]

#     def test_sqrt_from_10_power_100_to_10_power_1000(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat(From=10**100, To=10**1000, sign=0)
#             true_a = self.make_decimal_from_Bigfloat(a)
#             true_sqrt = str(true_a.sqrt())
#             test_sqrt = Bigfloat.sqrt(a)
#             test_sqrt = str(self.make_decimal_from_Bigfloat(test_sqrt))
#             assert true_sqrt[:10000] == test_sqrt[:10000]

#     def test_sqrt_from_10_power_1000_to_10_power_10000(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat(From=10**1000, To=10**10000, sign=0)
#             true_a = self.make_decimal_from_Bigfloat(a)
#             true_sqrt = str(true_a.sqrt())
#             test_sqrt = Bigfloat.sqrt(a)
#             test_sqrt = str(self.make_decimal_from_Bigfloat(test_sqrt))
#             assert true_sqrt[:10000] == test_sqrt[:10000]

    
#     def test_sqrt_from_one(self):
#         for i in range(self.COUNT_TESTS):
#             one = Bigfloat([1])
#             test_sqrt = Bigfloat.sqrt(one)
#             assert test_sqrt == one


#     def test_eq_with_same_exp(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_int(1, 10**10000)
#             b = self.generate_random_int(1, 10**10000)
#             Bigfloat_a = Bigfloat.make_Bigfloat_from_int(a)
#             Bigfloat_b = Bigfloat.make_Bigfloat_from_int(b)
#             true_answer = (a == b)
#             test_answer = (Bigfloat_a == Bigfloat_b)
#             assert true_answer == test_answer


#     def test_eq_with_different_exp(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat()
#             b = self.generate_random_Bigfloat()
#             test_answer = (a == b)
#             true_a = self.make_decimal_from_Bigfloat(a)
#             true_b = self.make_decimal_from_Bigfloat(b)
#             true_answer = (true_a == true_b)
#             assert true_answer == test_answer

#     def test_ge_with_same_exp(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_int(1, 10**10000)
#             b = self.generate_random_int(1, 10**10000)
#             Bigfloat_a = Bigfloat.make_Bigfloat_from_int(a)
#             Bigfloat_b = Bigfloat.make_Bigfloat_from_int(b)
#             true_answer = (a >= b)
#             test_answer = (Bigfloat_a >= Bigfloat_b)
#             assert true_answer == test_answer


#     def test_ge_with_different_exp(self):
#         for i in range(self.COUNT_TESTS):
#             a = self.generate_random_Bigfloat()
#             b = self.generate_random_Bigfloat()
#             test_answer = (a >= b)
#             true_a = self.make_decimal_from_Bigfloat(a)
#             true_b = self.make_decimal_from_Bigfloat(b)
#             true_answer = (true_a >= true_b)
#             assert true_answer == test_answer

    




class TestQuadraticEquation(unittest.TestCase, SupportFunctions):

    COUNT_TESTS = 100
    PRECISION_DIGITS = 10000

    def reference_solve_decimal(self, a_dec, b_dec, c_dec):
        if a_dec == 0:
            if b_dec == 0:
                return None
            x = -c_dec / b_dec
            return (x,)
        D = b_dec * b_dec - Decimal(4) * a_dec * c_dec
        if D < 0:
            return None
        sqrt_D = D.sqrt()
        x1 = (-b_dec + sqrt_D) / (Decimal(2) * a_dec)
        x2 = (-b_dec - sqrt_D) / (Decimal(2) * a_dec)
        return (x1, x2)

    def compare_decimal_values(self, ref, test, precision):
        ref_s = str(ref)
        test_s = str(test)
        match_len = min(precision, len(ref_s), len(test_s))
        self.assertEqual(ref_s[:match_len], test_s[:match_len],
                         "Не совпали первые {0} символов:\nref  = {1}\ntest = {2}".format(
                             match_len, ref_s[:match_len + 20], test_s[:match_len + 20]))

    def run_and_compare(self, a_int, b_int, c_int, precision=None):
        if precision is None:
            precision = self.PRECISION_DIGITS
        a_dec = Decimal(a_int)
        b_dec = Decimal(b_int)
        c_dec = Decimal(c_int)
        ref = self.reference_solve_decimal(a_dec, b_dec, c_dec)
        self.assertIsNotNone(ref, "D < 0, тест должен генерировать D >= 0")

        data = Data("{0} {1} {2}".format(a_int, b_int, c_int))
        answer = solve(data)

        if len(ref) == 1:
            self.assertEqual(answer.get_message(), Messages.EQUATION_HAS_ONLY_ONE_ROOT)
            prog_x1 = self.make_decimal_from_Bigfloat(answer.get_x1())
            self.compare_decimal_values(ref[0], prog_x1, precision)
        else:
            ref_x1, ref_x2 = ref
            prog_x1 = self.make_decimal_from_Bigfloat(answer.get_x1())
            msg = answer.get_message()
            if msg == Messages.EQUATION_HAS_TWO_SAME_ROOTS:
                self.assertEqual(ref_x1, ref_x2)
                self.compare_decimal_values(ref_x1, prog_x1, precision)
            else:
                self.assertIsNone(msg)
                prog_x2 = self.make_decimal_from_Bigfloat(answer.get_x2())
                self.compare_decimal_values(ref_x1, prog_x1, precision)
                self.compare_decimal_values(ref_x2, prog_x2, precision)

    # def test_two_real_roots_known_values(self):
    #     self.run_and_compare(1, 5, 6, precision=100)
    #     self.run_and_compare(1, -7, 12, precision=100)
    #     self.run_and_compare(2, 7, 3, precision=100)
    #     self.run_and_compare(1, 0, -4, precision=100)

    def test_two_real_roots_small_int(self):
        for i in range(self.COUNT_TESTS):
            while True:
                a = self.generate_random_int(10**9999, 10**10000)
                b = self.generate_random_int(10**9999, 10**10000)
                c = self.generate_random_int(10**9999, 10**10000)
                D = Decimal(b) * Decimal(b) - Decimal(4) * Decimal(a) * Decimal(c)
                if D > 0:
                    break
            self.run_and_compare(a, b, c)

    def test_two_real_roots_medium_int(self):
        for i in range(self.COUNT_TESTS):
            while True:
                a = self.generate_random_int(10**9999, 10**10000)
                b = self.generate_random_int(10**9999, 10**10000)
                c = self.generate_random_int(10**9999, 10**10000)
                D = Decimal(b) * Decimal(b) - Decimal(4) * Decimal(a) * Decimal(c)
                if D > 0:
                    break
            self.run_and_compare(a, b, c)

    def test_two_real_roots_large_int(self):
        for i in range(self.COUNT_TESTS):
            while True:
                a = self.generate_random_int(10**9999, 10**10000)
                b = self.generate_random_int(10**9999, 10**10000)
                c = self.generate_random_int(10**9999, 10**10000)
                D = Decimal(b) * Decimal(b) - Decimal(4) * Decimal(a) * Decimal(c)
                if D > 0:
                    break
            self.run_and_compare(a, b, c)

    # def test_two_equal_roots(self):
    #     for i in range(self.COUNT_TESTS):
    #         k = self.generate_random_int(10**4999, 10**5000, sign=0)
    #         m = self.generate_random_int(10**4999, 10**5000, sign=0)
    #         a = k * k
    #         c = m * m
    #         b = 2 * k * m
    #         self.run_and_compare(a, b, c)

    def test_linear_equation(self):
        for i in range(self.COUNT_TESTS):
            b = self.generate_random_int(10**9999, 10**10000)
            c = self.generate_random_int(10**9999, 10**10000)
            self.run_and_compare(0, b, c)

    def test_two_real_roots_negative_coefficients(self):
        for i in range(self.COUNT_TESTS):
            while True:
                a = self.generate_random_int(10**9999, 10**10000)
                b = self.generate_random_int(10**9999, 10**10000)
                c = self.generate_random_int(10**9999, 10**10000)
                a *= choice([-1, 1])
                b *= choice([-1, 1])
                c *= choice([-1, 1])
                D = Decimal(b) * Decimal(b) - Decimal(4) * Decimal(a) * Decimal(c)
                if D > 0:
                    break
            self.run_and_compare(a, b, c)


class BenchmarkBigfloat(SupportFunctions):


    def __init__(self):
        self.test_run_time_add()
        self.test_run_time_sub()
        self.test_run_time_mul()
        self.test_run_time_div()
        self.test_run_time_sqrt()

    def test_run_time_add(self):
        a = self.generate_random_Bigfloat(From=10 ** 9999, To=10 ** 10000)
        b = self.generate_random_Bigfloat(From=10 ** 9999, To=10 ** 10000)
        time1 = perf_counter()
        c = a + b
        time2 = perf_counter()
        print("время выполнения сложения 2 чисел с 10000 знаков: {0}".format(time2 - time1))

    def test_run_time_sub(self):
        a = self.generate_random_Bigfloat(From=10 ** 9999, To=10 ** 10000)
        b = self.generate_random_Bigfloat(From=10 ** 9999, To=10 ** 10000)
        time1 = perf_counter()
        c = a - b
        time2 = perf_counter()
        print("время выполнения вычитания 2 чисел с 10000 знаков: {0}".format(time2 - time1))

    def test_run_time_mul(self):
        a = self.generate_random_Bigfloat(From=10 ** 9999, To=10 ** 10000)
        b = self.generate_random_Bigfloat(From=10 ** 9999, To=10 ** 10000)
        time1 = perf_counter()
        c = a * b
        time2 = perf_counter()
        print("время выполнения умножения 2 чисел с 10000 знаков: {0}".format(time2 - time1))

    def test_run_time_div(self):
        a = self.generate_random_Bigfloat(From=10 ** 9999, To=10 ** 10000)
        b = self.generate_random_Bigfloat(From=10 ** 9999, To=10 ** 10000)
        time1 = perf_counter()
        c = a / b
        time2 = perf_counter()
        print("время выполнения деления 2 чисел с 10000 знаков: {0}".format(time2 - time1))

    def test_run_time_sqrt(self):
        a = self.generate_random_Bigfloat(From=10 ** 9999, To=10 ** 10000)
        time1 = perf_counter()
        c = Bigfloat.sqrt(a)
        time2 = perf_counter()
        print("время вычисления корня числа с 10000 знаков: {0}".format(time2 - time1))

    

if __name__ == "__main__":
    a = BenchmarkBigfloat()
    unittest.main()
    
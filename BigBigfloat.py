from __future__ import annotations
from FFT import FFT_ROOTS
from typing import TypeAlias
import sys
import math
from typing import Any


from copy import deepcopy

list_of_int: TypeAlias = list[int]
sys.set_int_max_str_digits(0)

class Bigfloat:
    """
    Класс поддерживающий длинную арифметику.
    
    Поддерживает операции сложения, вычитания, умножения, 
    деления и вычисления корня для чисел до 10000 знаков.


    Параметры
    __________________________________________________
    
    Параметр 1:
    number: Является списком, содержащим мантиссу числа. 
    Значения в списке хранятся блоками, по 6 цифр числа в каждом блоке.
    Значения в списке идут от самых младших разрядов числа к старшим.
    По умолчанию пустой список.

    Параметр 2:
    exp: Число, означающее на какую степень десятки домножить мантиссу для получения хранимого числа.
    По умолчанию 0.
    
    Параметр 3:
    negative: Булево значение, если True - число отрицательное, иначе положительное.
    По умолчанию False.



    Атрибуты
    __________________________________________________

    Атрибут 1:
    BASE: Константа, означающая разрядность одного блока в number.

    Атрибут 2:
    power_BASE: Предрассчитанное значение 10 в степени BASE.
    Требуется для арифметических операций, обработки переносов.

    """
    __slots__ = ["number", "exp", "negative", "kind"]

    BASE = 5
    power_BASE = 10 ** BASE


    def __init__(self,
                 number: list_of_int = None,
                 exp: int = 0,
                 negative: bool = False,
                 kind: str = "finite"):
        
        """Инициализирует объект, удаляет незначащие нули, приводит exp к значению, кратному BASE."""
        self.number = number if number is not None else []
        self.exp = exp
        self.negative = negative
        self.kind = kind
        if kind == "finite":
            self._make_exp_multiple_BASE()

    
    def get_mantissa(self):
        return self.number
    
    def get_exp(self):
        return self.exp
    
    def is_negative(self):
        return self.negative
    def is_finite(self) -> bool:
        return self.kind == "finite"

    def is_nan(self) -> bool:
        return self.kind == "nan"

    def is_inf(self) -> bool:
        return self.kind == "inf"

    @classmethod
    def make_inf(cls, negative: bool = False) -> Bigfloat:
        return cls([0], 0, negative, "inf")

    @classmethod
    def make_nan(cls) -> Bigfloat:
        return cls([0], 0, False, "nan")

    @classmethod
    def make_Bigfloat_from_int(self,
                               other: int) -> Bigfloat:
        
        """Создает из числа типа int число типа Bigfloat."""
        other_work = str(other)
        result_negative = False
        if other_work[0] == "-":
            result_negative = True
            other_work = other_work[1:]
        other_work = other_work[::-1]
        result_number = []
        result_exp = 0
        while other_work != "":
            element = other_work[:self.BASE]
            element = element[::-1]
            element = int(element)
            other_work = other_work[self.BASE:]
            result_number.append(element)
        return Bigfloat(result_number, result_exp, result_negative)
    

    def __eq__(self, 
               value: Any) -> bool:
        
        """Принимает на вход либо тип Bigfloat, либо int, для остальных выбрасывает ошибку."""
        if type(value) == int:
            Bigfloat_value = Bigfloat.make_Bigfloat_from_int(value)
        elif type(value) == Bigfloat:
            Bigfloat_value = value
        else:
            raise ValueError("некорректное сравнение")
        return (self.kind == Bigfloat_value.kind and
                self.negative == Bigfloat_value.negative and
                self.number == Bigfloat_value.number and
                self.exp == Bigfloat_value.exp)



    def _make_digit_transfer(self) -> None:

        """Делает переносы разрядов. Если блок превысит power_BASE, то осуществляется перенос в следующий блок."""
        transfer = 0
        for i in range(len(self.number)):
            self.number[i] += transfer
            if self.number[i] >= self.power_BASE:
                transfer = self.number[i] // self.power_BASE
                self.number[i] = self.number[i] % self.power_BASE
            else:
                transfer = 0
        while transfer != 0:
            self.number.append(transfer % self.power_BASE)
            transfer //= self.power_BASE


        
    def _more_abs(self,
                  other: Bigfloat) -> bool: 
        
        """
        Производит сравнение двух чисел Bigfloat по модулю.
        Приводит exp двух чисел к кратным BASE.
        Считает сдвиг разрядов данных чисел.
        Если длина длина одного строго больше выдает True, если строго меньше False.
        Находит индекс самого первого значащего числа для сравнения.
        Находит индекс самого последнего значащего числа для сравнения.
        С учетом сдвига сравнивает числа поразрядно.
        """
        self._make_exp_multiple_BASE()
        other._make_exp_multiple_BASE()
        shift = self._calculate_shift(other)
        len_self = len(self.number)
        len_other = len(other.number)
        start_pos = min(shift, 0)
        end_pos = max(len_self - 1, len_other + shift - 1)
        for i in range(end_pos, start_pos - 1, -1):
            elem_a = self.number[i] if 0 <= i < len_self else 0
            b_ind = i - shift
            elem_b = other.number[b_ind] if 0 <= b_ind < len_other else 0
            if elem_a > elem_b:
                return True
            elif elem_a < elem_b:
                return False
        return False



    def _make_exp_multiple_BASE(self) -> None:
        
        """
        Приводит exp к кратному BASE.
        Необходимо для корректного высчитывания сдвига числа и удобного вывода числа.
        """
        new_exp = (self.exp // self.BASE) * self.BASE
        difference = 10 ** (self.exp - new_exp)
        for i in range(len(self.number)):
            self.number[i] = self.number[i] * difference
        self._make_digit_transfer()
        self.exp = new_exp

    

    def _calculate_shift(self,
                         other: Bigfloat) -> int:
        
        """Считает сдвиг разрядов двух чисел из-за exp."""
        difference = other.exp - self.exp
        shift = difference // self.BASE
        return shift
    


    def take_first_digits_for_approximation_and_exp(self) -> tuple[int, int]:

        """
        Возвращает кортеж 2 значений.
        Первое значение содержит 1 или 2 старших блока number, объединенных в 1 int.
        Второе значение содержит количество блоков в number за исключением первых.

        Пример:
        [123456, 789012, 345678, 901234] -> tuple(901234345678, 2)
        """
        exp = self.exp
        len_self = len(self.number)
        if len_self < 2:
            digit = self.number[-1]
        elif len_self < 3:
            digit = self.number[-1] * self.power_BASE + self.number[-2]
            exp += ((len_self - 2) * self.BASE)
        else:
            digit = self.number[-1] * (self.power_BASE ** 2) + self.number[-2] * self.power_BASE + self.number[-3]
            exp += ((len_self - 3) * self.BASE)
        return digit, exp
    


    def _delete_minor_zeros(self) -> None:

        """
        Удаляет слева и справа списка number незначащие нули.
        Если ноль был слева, в exp числа записывается дополнительно значение BASE.
        Если справа, ноль удаляется из списка.
        """
        while len(self.number) > 0 and self.number[-1] == 0:
            self.number.pop()
        while len(self.number) > 0 and self.number[0] == 0:
            self.number.pop(0)
            self.exp += self.BASE
        if not self.number:
            self.number = [0]
            self.exp = 0
            self.negative = False
        


    def take_first_division_approximation_and_exp(self,
                                                  scale: int) -> tuple[int, int]:
        
        """
        Возвращает кортеж 2 значений.
        Первое значение содержит первое приближение 1/само число.
        Scale означает exp данного приближения, чтобы избежать работу c неточными float.
        """

        top_digit, exp = self.take_first_digits_for_approximation_and_exp()
        first_approximation = (10 ** scale) // top_digit
        return first_approximation, -(exp + scale)
    


    def _is_zero(self) -> bool:
        return self.kind == "finite" and all(d == 0 for d in self.number)
    


    def remove_extra_digits(self,
                            accuracy: int) -> None:
        
        """
        Используется при вычислении операций деления и умножения.
        Квадратичная сходимость данных операций позволяет для экономии времени обрезать неточные значения, сохраняя лишь точный результат.
        """
        len_self = len(self.number)
        if len_self > accuracy:
            cut = len_self - accuracy
            self.number = self.number[cut:]
            self.exp += (cut * self.BASE)

        

    def Newton_method(self) -> Bigfloat:

        """
        Возвращает точное приближение 1/само число.
        Точность составляет 10000 знаков.
        Изначально берет примерное значение 1/само число, 
        затем c помощью итеративного алгоритма Ньютона уточняет первое приближение.
        """
        SCALE = self.BASE * 6
        digit = deepcopy(self)
        digit._make_exp_multiple_BASE()
        first_approximation, exp = digit.take_first_division_approximation_and_exp(SCALE)
        x = Bigfloat.make_Bigfloat_from_int(first_approximation)
        x.exp = exp
        x.negative = digit.negative
        accuracy = len(x.number)
        for i in range(11):
            target_len = accuracy * (2 ** i)
            two = Bigfloat([2], 0)
            rounded_digit = deepcopy(digit)
            rounded_digit.remove_extra_digits(target_len + 10)
            x = x * (two - rounded_digit * x)
            x.remove_extra_digits(target_len)
        x.remove_extra_digits(target_len)
        return x
        


    def _add_digits(self,
                    other: Bigfloat) -> Bigfloat:
        
        """
        Складывает два числа столбиком с учетом сдвига разрядов, также учитывается перенос разрядов.
        Считает сдвиг разрядов данных чисел.
        Находит индекс самого первого значащего числа для сложения.
        Находит индекс самого последнего значащего числа для сложения.
        С учетом сдвига складывает числа поразрядно.
        Оба числа положительные.
        """
        shift = self._calculate_shift(other)
        result_number = []
        len_other = len(other.number)
        len_self = len(self.number)
        start_pos = min(shift, 0)
        end_pos = max(len_self, len_other + shift)
        transfer = 0
        for i in range(start_pos, end_pos):
            elem_a = self.number[i] if 0 <= i < len_self else 0
            b_ind = i - shift
            elem_b = other.number[b_ind] if 0 <= b_ind < len_other else 0
            summ = elem_a + elem_b + transfer
            if summ >= self.power_BASE:
                transfer = summ // self.power_BASE
                summ %= self.power_BASE
            else:
                transfer = 0
            result_number.append(summ)
        if transfer != 0:
            result_number.append(transfer)
        result = Bigfloat(result_number, exp=min(self.exp, other.exp))
        result._delete_minor_zeros()
        return result
        
    

    def _substract_digits(self,
                          other: Bigfloat) -> Bigfloat:
        
        """
        Вычитает два числа столбиком с учетом сдвига разрядов, также учитывается заем разрядов.
        Считает сдвиг разрядов данных чисел.
        Находит индекс самого первого значащего числа для вычитания.
        Находит индекс самого последнего значащего числа для вычитания.
        С учетом сдвига вычитает числа поразрядно.
        Первое число больше либо равно по модулю второго.
        """
        if self == other:
            return Bigfloat([0])
        shift = self._calculate_shift(other)
        result_number = []
        len_other = len(other.number)
        len_self = len(self.number)
        start_pos = min(shift, 0)
        end_pos = max(len_self, len_other + shift)
        loan = 0
        for i in range(start_pos, end_pos):
            elem_a = self.number[i] if 0 <= i < len_self else 0
            b_ind = i - shift
            elem_b = other.number[b_ind] if 0 <= b_ind < len_other else 0
            difference = elem_a - elem_b - loan
            if difference < 0:
                difference += self.power_BASE
                loan = 1
            else:
                loan = 0
            result_number.append(difference)
        result = Bigfloat(result_number, exp=min(self.exp, other.exp))
        result._delete_minor_zeros()
        return result
        


    def take_first_approximation_for_sqrt(self,
                                          scale: int = 15) -> Bigfloat: 
        
        """Ищет первое приближение 1/sqrt(само число)."""
        top_digit, exp = self.take_first_digits_for_approximation_and_exp()
        if exp % 2 != 0:
            top_digit *= 10
            exp -= 1
        approx_sqrt = int(math.sqrt(top_digit) * (10 ** scale))
        first_approximation = (10 ** (scale * 2)) // approx_sqrt
        first_approximation = Bigfloat.make_Bigfloat_from_int(first_approximation)
        first_approximation.exp += (-(scale) - (exp // 2))
        return first_approximation



    def divide_by_two(self) -> None:

        """Быстрое деление числа на 2."""
        len_self = len(self.number)
        for i in range(len_self):
            self.number[i] *= 5
        self._make_digit_transfer()
        self.exp = self.exp - 1

        
    def _is_one(self) -> bool:
        return self.number == [1] and self.exp == 0 
    

    def sqrt(self) -> Bigfloat:
        
        """С помощью итеративного алгоритма Ньютона уточняет первое приближение 1/sqrt(само число) до точности в 10000 знаков."""
        if self._is_one():
            return self
        self._make_exp_multiple_BASE()
        x = self.take_first_approximation_for_sqrt()
        accuracy = len(x.number)
        for i in range(11):
            three = Bigfloat([3], 0)
            num = deepcopy(self)
            num.remove_extra_digits(accuracy + 10)
            x = x * (three - num * (x * x))
            x.divide_by_two()
            accuracy *= 2
            x.remove_extra_digits(accuracy + 10)
        x.remove_extra_digits(accuracy + 10)
        num = deepcopy(self)
        num.remove_extra_digits(accuracy + 10)
        answer = num * x
        return answer


        
    def _add_Bigfloat_numbers(self,
                              other: Bigfloat) -> Bigfloat:
        
        """Подготавливает 2 числа к сложению и возвращает результат сложения."""
        self._make_exp_multiple_BASE()
        other._make_exp_multiple_BASE()
        self._delete_minor_zeros()
        other._delete_minor_zeros()
        result_number = self._add_digits(other)
        return result_number



    def _add_Bigfloat_numbers_with_same_sign(self,
                                             other: Bigfloat) -> Bigfloat:
        
        """Возвращает необходимый алгоритм для сложения чисел с одинаковыми знаками."""
        if self.negative is True:
            result = self._add_Bigfloat_numbers(other)
            result.negative = True
            return result
        else:
            return self._add_Bigfloat_numbers(other)
        


    def _add_Bigfloat_numbers_with_different_sign(self,
                                                  other: Bigfloat) -> Bigfloat: 
        
        """
        Возвращает необходимый алгоритм для сложения чисел с разными знаками.
        
        Пример:
        (5) + (-3) -> 5 - 3
        (-5) + (3) -> 3 - 5
        """
        self._make_exp_multiple_BASE()
        other._make_exp_multiple_BASE()
        self._delete_minor_zeros()
        other._delete_minor_zeros()
        if self.negative:
            if self._more_abs(other):
                result_number = self._substract_digits(other)
                if not result_number._is_zero():
                    result_number.negative = True
            else:
                result_number = other._substract_digits(self)

        else:
            if self._more_abs(other):
                result_number = self._substract_digits(other)
            else:
                result_number = other._substract_digits(self)
                if not result_number._is_zero():
                    result_number.negative = True
        return result_number
    


    def _substract_Bigfloat_numbers_with_different_sign(self,
                                                        other: Bigfloat) -> Bigfloat:
        
        """
        Возвращает необходимый алгоритм для вычитания чисел с разными знаками.
        
        Пример:
        (5) - (-3) -> 5 + 3
        (-5) - (3) -> -(3 + 5)
        """
        if self.negative:
            result = self._add_Bigfloat_numbers(other)
            result.negative = True
            return result
        else:
            result = self._add_Bigfloat_numbers(other)
            return result
        

    def reverse_sign(self) -> None:
        self.negative = not self.negative
  

    def __ge__(self, 
               value: Any) -> bool:
        
        """
        Сравнивает больше ли или равно одно число другому.
        На ввод может получать int или Bigfloat, иначе выдает ошибку.
        """
        if type(value) == int:
            Bigfloat_value = Bigfloat.make_Bigfloat_from_int(value)
        elif type(value) == Bigfloat:
            Bigfloat_value = value
        else:
            raise ValueError("некорректное сравнение")
        if Bigfloat_value == self:
            return True
        if Bigfloat_value.negative is not self.negative:
            if Bigfloat_value.negative:
                return True
            else:
                return False
        if Bigfloat_value.negative:
            return Bigfloat_value._more_abs(self)
        return self._more_abs(Bigfloat_value)
        
        

    def __add__(self,
                other: Bigfloat):
        
        """Проверяет два числа на знаки и в зависимости от этого выбирает алгоритм для сложения."""
        if self._is_zero():
            return other
        if other._is_zero():
            return self
        if self.negative is not other.negative:
            return self._add_Bigfloat_numbers_with_different_sign(other)
        else:
            return self._add_Bigfloat_numbers_with_same_sign(other)
        


    def __sub__(self,
                      other: Bigfloat):
        
        """Проверяет два числа на знаки и в зависимости от этого выбирает алгоритм для вычитания."""
        if self._is_zero():
            answer = deepcopy(other)
            answer.negative = not answer.negative
            return answer
        if other._is_zero():
            return self
        self._delete_minor_zeros()
        other._delete_minor_zeros()
        if self.negative is not other.negative:
            return self._substract_Bigfloat_numbers_with_different_sign(other)
        else:
            return self._add_Bigfloat_numbers_with_different_sign(other)
        
    

    def __mul__(self,
                other: Bigfloat):
        
        """Умножает 2 числа с помощью алгоритма дискретного разложения Фурье."""
        self._make_exp_multiple_BASE()
        other._make_exp_multiple_BASE()
        result = Bigfloat()
        result.number = FFT_ROOTS.multiply(self.number[:], other.number[:])
        result.exp = self.exp + other.exp
        result.negative = self.negative ^ other.negative
        return result
    


    def __truediv__(self,
                    divider: Bigfloat):    
        
        """Для случаев когда делимое равно делителю возвращает 1, иначе делит 2 числа алгоритмом Ньютона."""
        if self.number == divider.number and self.exp == divider.exp:
            if self.negative is not divider.negative:
                return Bigfloat([1], negative=True)
            else:
                return Bigfloat([1], negative=False)
        answer = self * divider.Newton_method() 
        answer._delete_minor_zeros()
        return answer
    

    def __str__(self):

        """
        Выводит число типа Bigfloat на экран. 
        Если блок не состоит из BASE цифр, то дополняем нулями и добавляем к итоговой строке.
        Если экспонента положительна в конце строки дописываем нули.
        Если экспонента отрицательна и по модулю больше длины числа, то сначала дописываем нули и ставим точку после первого нуля.
        Если экспонента отрицательна и по модулю меньше длины числа, то ставим точку в самом числе.

        """
        if self.is_nan():
            return "nan"
        if self.is_inf():
            return "-inf" if self.negative else "inf"
        str_digit = ""
        for x in reversed(self.number):
            str_digit += str(x).zfill(self.BASE)
        if self.exp >= 0:
            str_digit += "0" * self.exp
        else:
            if len(str_digit) <= abs(self.exp):
                str_digit = "0." + "0" * (abs(self.exp) - len(str_digit)) + str_digit
            else:
                point = len(str_digit) - abs(self.exp)
                str_digit = str_digit[:point] + "." + str_digit[point:]
        if str_digit == "" or str_digit == ".":
            str_digit = "0"
        point_zero = 0
        while (point_zero + 1 < len(str_digit) and
               str_digit[point_zero] == "0" and
               str_digit[point_zero + 1] != "."):
            point_zero += 1
        str_digit = str_digit[point_zero:]
        if self.negative:
            str_digit = "-" + str_digit
        
        return str_digit

            





    













    
    

    
    


    
        

        







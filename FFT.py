import math
import cmath

POWER_TWO_TABLE = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536]
POWER_TWO = 16
MAX_LENGTH_NUMBER = 2 ** POWER_TWO
TWO_PI = -2 * math.pi


class FFT:

    power_BASE = 10 ** 5
    BASE = 5


    def __init__(self):

        self.roots = []
        self.inverse_roots = []
        self.bit_reverse = []
        self._count_w()
        self._precalculate_bit_reverse()


    def _count_w(self) -> None:
        size_number = 2
        while size_number <= MAX_LENGTH_NUMBER:
            angle = TWO_PI / size_number
            base_root = cmath.rect(1.0, angle)
            base_inverse_root = base_root.conjugate()
            root = [1] * (size_number // 2)
            inverse_root = [1] * (size_number // 2)
            for i in range(1, size_number // 2):
                if i % 32 == 0:
                    angle = TWO_PI * i / size_number
                    root[i] = cmath.rect(1, angle)
                    inverse_root[i] = root[i].conjugate()
                else:
                    root[i] = root[i - 1] * base_root
                    inverse_root[i] = inverse_root[i - 1] * base_inverse_root
            self.roots.append(root)
            self.inverse_roots.append(inverse_root)
            size_number <<= 1

    
    def _precalculate_bit_reverse(self) -> None:
        power_two = 1
        while power_two <= POWER_TWO:
            size = POWER_TWO_TABLE[power_two - 1]
            cash = [0] * size
            bits = power_two
            for i in range(1, size):
                cash[i] = self._bit_reverse(i, bits)
            self.bit_reverse.append(cash)
            power_two += 1


    def _add_minor_zeros(self,
                         first_digit: list, 
                         second_digit: list) -> None:
                   
        length_first_digit = len(first_digit)
        length_second_digit = len(second_digit)
        result_len = length_first_digit + length_second_digit - 1
        n = 1 << (result_len - 1).bit_length()
        first_digit.extend([0] * (n - length_first_digit))
        second_digit.extend([0] * (n - length_second_digit))


    
    def _calculate_power_of_two(self,
                                digit: int) -> int:
        
        return digit.bit_length()
        

    def _bit_reverse(self,
                     number: int,
                     bits: int) -> int:

        reversed_num = 0
        for _ in range(bits):
            reversed_num = (reversed_num << 1) | (number & 1)
            number >>= 1
        return reversed_num
    


    def _bit_permutation_numbers(self,
                                first_digit: list) -> None:
        
        length_number = len(first_digit)
        k = (length_number - 1).bit_length()
        cash = self.bit_reverse[k - 1]
        for i in range(1, length_number):
            j = cash[i]
            if i < j:
                first_digit[i], first_digit[j] = first_digit[j], first_digit[i]



    def ntt(self,
            first_digit: list,
            reverse = False) -> None:
        
        length_number = len(first_digit)
        self._bit_permutation_numbers(first_digit)
        block_size = 2
        power_of_two = 0
        if reverse == False:
            roots = self.roots
        else:
            roots = self.inverse_roots
        while block_size <= length_number:
            step = block_size // 2
            w = roots[power_of_two]
            for i in range(0, length_number, block_size):
                for j in range(step):
                    u = first_digit[i + j]
                    v = first_digit[i + j + step] * w[j]
                    first_digit[i + j] = u + v
                    first_digit[i + j + step] = u - v
            block_size <<= 1
            power_of_two += 1 
        if reverse == True:
            n_inverse = 1 / length_number
            for i in range(length_number):
                first_digit[i] = first_digit[i] * n_inverse

    def irrft(self,
              list_of_numbers: list[complex]) -> list:
        

        len_list_of_number = len(list_of_numbers)
        if len_list_of_number == 1:
            n = 1
        else:
            n = (len_list_of_number - 1) * 2
        result_number = [0j] * n
        for i in range(len_list_of_number):
            result_number[i] = list_of_numbers[i]
        for i in range(1, n // 2):
            result_number[n - i] = list_of_numbers[i].conjugate()
        self.ntt(result_number, reverse=True)
        return [(x).real for x in result_number]
        


    def unpack_ntt(self,
             first_number: list[complex]) -> list:
        
        n = len(first_number)
        half = n // 2
        result_first = [0j] * (half + 1)
        result_second = [0j] * (half + 1)
        for i in range(half + 1):
            if i == 0:
                result_first[i] = complex(first_number[0].real, 0)
                result_second[i] = complex(first_number[0].imag, 0)
            elif i == half:
                result_first[i] = complex(first_number[half].real, 0)
                result_second[i] = complex(first_number[half].imag, 0)
            else:
                p = first_number[i]
                q = first_number[n - i].conjugate()
                result_first[i] = 0.5 * (p + q)
                result_second[i] = 0.5 * (-1j) * (p - q)
        return result_first, result_second



    def _normalize(self,
                   digit: list) -> None:
        
        transfer = 0  
        for i in range(len(digit)):
            digit[i] += transfer
            if digit[i] >= self.power_BASE:
                transfer, digit[i] = divmod(digit[i], self.power_BASE)
            else:
                transfer = 0
        while transfer != 0:
            transfer, digit_ = divmod(transfer, self.power_BASE)
            digit.append(digit_)
            

    


    def multiply(self,
                 first_number: list, 
                 second_number: list) -> list:

        

        length_of_result = len(first_number) + len(second_number) - 1
        self._add_minor_zeros(first_number, second_number)
        n = len(first_number)
        packed = [complex(first_number[i], second_number[i]) for i in range(n)]
        self.ntt(packed)
        spectr_first, spectr_second = self.unpack_ntt(packed)
        result_number = [spectr_first[i] * spectr_second[i] for i in range(len(spectr_first))]
        result_number = self.irrft(result_number)
        result_number = result_number[:length_of_result]
        result_number = [int(round(x)) for x in result_number]
        self._normalize(result_number)
        return result_number



FFT_ROOTS = FFT()

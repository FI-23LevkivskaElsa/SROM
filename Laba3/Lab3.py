import timeit

a = "00110001101111001000010000011001100000101101101101101110010011111001001000101010011101111011101110110100111101111101101011100100111101001001100011110110000110011001001110010011101011111000111010000000010111100100000110111100100010111010111110001101100001101010110100100111111100111110101101001"
b = "00111110100000001111101000011111101101101111010111111010111001100000000001000001110111001111001010000110111001101110100110011011000011001010110010011110010111001010011011110111110011111000011110100000011000011111001101111011110100011111101101011101000011011010110001000000101101111101011101101"
n = "11100011001010010101110001111000001100001101010111100100011001001000011101111001000101111111101101011100101110010010101100011101010001110010001000000101101111111011000010011000101010011010010000010111100000101000101100111000111011010101001111010011101101101101001101111101011100111110100110111"

p = "100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100001000011"

a = [int(char) for char in a][::-1]
b = [int(char) for char in b][::-1]
p = [int(char) for char in p][::-1]


class GF2_293:
    def __init__(self, m, irr_poly):
        self.m = m
        self.irr_poly = irr_poly

    def add_sub(self, num1, num2):
        n = max(len(num1), len(num2))
        if len(num1) > len(num2):
            num2 = num2 + [0] * abs(len(num1) - len(num2))
        if len(num1) < len(num2):
            num1 = num1 + [0] * abs(len(num1) - len(num2))

        C = []
        for i in range(n):
            temp = num1[i] + num2[i]
            C.append(temp % 2)

        return C

    def mul_one_digit (self, num1, digit):
        C = []
        for i in range(len(num1)):
            temp = num1[i] * digit
            C.append(temp % 2)
        return C

    def mul(self, num1, num2):
        n = len(num2)
        C = []
        for i in range(n):
            temp = self.mul_one_digit(num1, num2[i])
            temp = [0] * i + temp
            C = self.add_sub(C, temp)
        _, C = self.div_mod(C, self.irr_poly)
        return C

    def normalize(self, num):
        while len(num) > 1 and num[-1] == 0:
            num.pop()
        return num

    def cmp(self, num1, num2):
        num1, num2 = self.normalize(num1), self.normalize(num2)
        n = max(len(num1), len(num2))
        if len(num1) > len(num2):
            num2 = num2 + [0] * abs(len(num1) - len(num2))
        if len(num1) < len(num2):
            num1 = num1 + [0] * abs(len(num1) - len(num2))
        i = n - 1
        while num1[i] == num2[i] and i > -1:
            i = i - 1
        if i == -1:
            return 0
        else:
            if num1[i] > num2[i]:
                return 1
            else:
                return -1

    def div_mod(self, num1, num2):
        k = len(num2)
        R = num1
        Q = [0] * len(num1)
        while self.cmp(R, num2) >= 0:
            t = len(R)
            C = [0] * (t - k) + num2
            if self.cmp(R, C) < 0:
                t = t - 1
                C = [0] * (t - k) + num2
            R = self.add_sub(R, C)
            Q[(t - k)] = Q[(t - k)] | 1
        return Q, R

    def power_2(self, num):
        n = len(num)
        C = []
        for i in range(n):
            C = C + [num[i]] + [0]
        _, C = self.div_mod(C, self.irr_poly)
        return C

    def inverted_element(self, num):
        C = [1]
        m = bin((2 ** self.m) - 2).lstrip("0b")
        for i in range(len(m) - 1, -1, -1):
            if m[i] == '1':
                C = self.mul(num, C)
            num = self.power_2(num)
        return C

    def power_horner(self, num, n):
        C = [1]
        for i in range(len(n) - 1, -1, -1):
            if n[i] == '1':
                C = self.mul(num, C)
            num = self.power_2(num)
        return C


def list_to_str(num_list):
    decimal_value = 0
    for i, block in enumerate(num_list):
        decimal_value = decimal_value + block * (2 ** i)
    str_num = bin(decimal_value).lstrip("0b")
    return str_num or "0"


m = 293
gf = GF2_293(m, p)

sum = gf.add_sub(a, b)
print("A + B = ", list_to_str(sum))

mul = gf.mul(a, b)
print("A * B = ", list_to_str(mul))

power = gf.power_2(a)
print("A ^ 2 = ", list_to_str(power))

inverted = gf.inverted_element(a)
print("A ^(-1) = ", list_to_str(inverted))

horner = gf.power_horner(a, n)
print("A ^ N = ", list_to_str(horner))


#ПЕРЕВІРКА
"""n = [int(char) for char in n]

test1 = gf.mul(gf.add_sub(a, b), n)
print("(A + B) * N =", list_to_str(test1))

test2 = gf.add_sub(gf.mul(b, n), gf.mul(n, a))
print("B * N + N * A =", list_to_str(test2))

test = gf.power_horner(n, bin(2**m - 1).lstrip("0b"))
print("N ^(2^m - 1) =", list_to_str(test))"""

#TIME
"""sum = timeit.timeit('gf.add_sub(a, b)', globals=globals(), number=10)
print(f"Час виконання операції : {sum} секунд для 10 операцій")

mul = timeit.timeit('gf.mul(a, b)', globals=globals(), number=10)
print(f"Час виконання операції : {mul} секунд для 10 операцій")

power = timeit.timeit('gf.power_2(a)', globals=globals(), number=10)
print(f"Час виконання операції : {power} секунд для 10 операцій")

inverted = timeit.timeit('gf.inverted_element(a)', globals=globals(), number=10)
print(f"Час виконання операції : {inverted} секунд для 10 операцій")

horner = timeit.timeit('gf.power_horner(a, n)', globals=globals(), number=10)
print(f"Час виконання операції : {horner} секунд для 10 операцій")"""

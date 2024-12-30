import numpy as np
import timeit

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_primitive_root(base, p):
    if not is_prime(p):
        return False
    required_set = set(range(1, p))
    result_set = set(pow(base, i, p) for i in range(1, p))
    return result_set == required_set

def check_onb_existence(m):
    p = 2 * m + 1
    if not is_prime(p):
        return f"Число p = {p} не є простим. ОНБ не існує."
    if is_primitive_root(2, p):
        return f"Число p = {p} є простим, і 2 є примітивним коренем модулю {p}. ОНБ існує."
    else:
        return f"Число p = {p} є простим, але 2 не є примітивним коренем модулю {p}. ОНБ не існує."


class GF2_ONB:
    def __init__(self, m):
        self.m = m
        self.p = (2 * m) + 1
        self.matrix = self.generate_matrix()

    def generate_matrix(self):
        matrix = np.zeros((self.m, self.m), dtype=int)
        for i in range(self.m):
            for j in range(self.m):
                if ((2 ** i - 2 ** j) % self.p == 1 or (2 ** i + 2 ** j) % self.p == 1 or (-2 ** i - 2 ** j) % self.p == 1 or (-2 ** i + 2 ** j) % self.p == 1):
                    matrix[i, j] = 1
        return matrix

    def add_sub(self, num1, num2):
        n = max(len(num1), len(num2))
        if len(num1) > len(num2):
            num2 = [0] * abs(len(num1) - len(num2)) + num2
        if len(num1) < len(num2):
            num1 = [0] * abs(len(num1) - len(num2)) + num1
        C = []
        for i in range(n):
            temp = num1[i] + num2[i]
            C.append(temp % 2)
        return C

    def mul(self, num1, num2):
        C = np.zeros(self.m, dtype=int)
        for i in range(self.m):
            N1 = np.array(num1, dtype=int)
            N2 = np.array(num2, dtype=int).reshape(-1, 1)
            C[i] = (N1 @ self.matrix @ N2) % 2
            num1 = num1[-(self.m - 1):] + num1[:1]
            num2 = num2[-(self.m - 1):] + num2[:1]
        return list(C)

        """C = [0] * self.m
        for i in range(self.m):
            temp = 0
            for j in range(self.m):
                for k in range(self.m):
                    temp = temp + num1[j] * self.matrix[j, k] * num2[k]
            C[i] = temp % 2
            num1 = num1[-(self.m - 1):] + num1[:1]
            num2 = num2[-(self.m - 1):] + num2[:1]
        return C"""

    def power_2(self, num):
        num = num[(self.m - 1):] + num[:(self.m - 1)]
        return num

    def inverted_element(self, num):
        beta = num
        k = 1
        m = bin(self.m - 1).lstrip("0b")
        t = len(m)
        for i in range(1, t):
            b = beta
            for p in range(k):
                b = self.power_2(b)
            beta = self.mul(b, beta)
            k = 2 * k
            if m[i] == "1":
                beta = self.mul(self.power_2(beta), num)
                k = k + 1
        return self.power_2(beta)

    def power_horner(self, num, n):
        C = [1] * (self.m)
        for i in range(len(n) - 1, -1, -1):
            if n[i] == '1':
                C = self.mul(C, num)
            num = self.power_2(num)
        return C

m = 293
gf_onb = GF2_ONB(m)

print(check_onb_existence(m))

print("Мультиплікативна матриця Λ:")
print(gf_onb.matrix)

a = "00010010111000010100101000011000110110001011010100101111111011011110001000011100110011100011011010011000000101001011111011001110011111101100100001101010011001100001101101111010000100110111100010010010010001110110010100000000000000010000001111001100001010101111010000101101011101110011101000001"
b = "01011111111101101000010011111100011101010101100100100001001001110011110011111001001110000011000100100101010101100001000100000101001110101010111001101011110111110111110100111011000000001011001111110000000111110011110111000101010011100100000010110101000000010101100111100111101000011001100010100"
n = "10011011110111000011100000001001111100111000111001001001011101101111100010111100011011101101011010111110011001001101110001111011001001001110011101101011110110000110100100001111010011001010101011011011000101011111111001100101101011001001101101000111101101001100101111110000001010111011100101110"

a = [int(char) for char in a]
b = [int(char) for char in b]

sum = gf_onb.add_sub(a, b)
print("A + B =", sum)

mul = gf_onb.mul(a, b)
print("A * B =", mul)

power = gf_onb.power_2(a)
print("A ^ 2 =", power)

inverted = gf_onb.inverted_element(a)
print("A ^(-1) =", inverted)

power_horner = gf_onb.power_horner(a, n)
print("A ^ N =", power_horner)

#ПЕРЕВІРКА
"""n = [int(char) for char in n]

test1 = gf_onb.mul(gf_onb.add_sub(a, b), n)
print("(A + B) * N =", test1)

test2 = gf_onb.add_sub(gf_onb.mul(b, n), gf_onb.mul(n, a))
print("B * N + N * A =", test2)

test = gf_onb.power_horner(n, bin(2**m - 1).lstrip("0b"))
print("N ^(2^m - 1) =", test)"""

#TIME
"""sum = timeit.timeit('gf_onb.add_sub(a, b)', globals=globals(), number=1)
print(f"Час виконання операції : {sum} секунд для 1 операцій")

mul = timeit.timeit('gf_onb.mul(a, b)', globals=globals(), number=1)
print(f"Час виконання операції : {mul} секунд для 1 операцій")

power = timeit.timeit('gf_onb.power_2(a)', globals=globals(), number=1)
print(f"Час виконання операції : {power} секунд для 1 операцій")

inverted = timeit.timeit('gf_onb.inverted_element(a)', globals=globals(), number=1)
print(f"Час виконання операції : {inverted} секунд для 1 операцій")

horner = timeit.timeit('gf_onb.power_horner(a, n)', globals=globals(), number=1)
print(f"Час виконання операції : {horner} секунд для 1 операцій")"""

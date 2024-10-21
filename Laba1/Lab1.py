a = str(input("Введіть значення А: "))
b = str(input("Введіть значення В: "))
#c = str(input("Введіть значення C: "))

def hex_to_32(hex_num, base=2**32):
    n = int(hex_num, 16)
    blocks = []
    while n > 0:
        blocks.append(n % base)
        n = n // base
    return blocks

a = hex_to_32(a)
b = hex_to_32(b)
#c = hex_to_32(c)

class LongNumOperations():
    def long_add(self, num1, num2, base=2**32):
        n = max(len(num1), len(num2))
        k = abs(len(num1) - len(num2))
        if len(num1) > len(num2):
            num2 = num2 + [0] * k
        if len(num1) < len(num2):
            num1 = num1 + [0] * k
        C = []
        carry = 0
        for i in range(n):
            temp = num1[i] + num2[i] + carry
            C.append(temp % base)
            carry = temp // base
        return C

    def long_sub(self, num1, num2, base=2**32):
        n = max(len(num1), len(num2))
        k = abs(len(num1) - len(num2))
        if len(num1) > len(num2):
            num2 = num2 + [0] * k
        if len(num1) < len(num2):
            num1 = num1 + [0] * k
        C = []
        borrow = 0
        for i in range(n):
            temp = num1[i] - num2[i] - borrow
            if temp >= 0:
                C.append(temp)
                borrow = 0
            else:
                C.append(base + temp)
                borrow = 1
        return C

    def long_mul_one_digit (self, num1, digit, base=2**32):
        C = []
        carry = 0
        for i in range(len(num1)):
            temp = num1[i] * digit + carry
            C.append(temp % base)
            carry = temp // base
        C.append(carry)
        return C

    def long_mul(self, num1, num2):
        n = max(len(num1), len(num2))
        C = []
        for i in range(n):
            temp = self.long_mul_one_digit(num1, num2[i])
            temp = [0] * i + temp
            C = self.long_add(C, temp)
        return C

    def long_cmp(self, num1, num2):
        n = max(len(num1), len(num2))
        k = abs(len(num1) - len(num2))
        if len(num1) > len(num2):
            num2 = num2 + [0] * k
        if len(num1) < len(num2):
            num1 = num1 + [0] * k
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

    """def long_div_mod(self, num1, num2):
        k = len(num2)
        R = num1
        Q = []
        if self.long_cmp(R, num2) >= 0:
            t = len(R)
            C = [0] * (t - k) + num2
            if self.long_cmp(R, C) == -1:
                t = t - 1
                C = [0] * (t - k) + num2
            R = self.long_sub(R, C)
            Q = self.long_add(Q, self.from10_to32(2**(t - k)))
        return Q

    def from10_to32(self, n, base=2 ** 32):
        blocks = []
        while n > 0:
            blocks.append(n % base)
            n = n // base
        return blocks"""

def from32_to16(num_32, base=2**32):
    decimal_value = 0
    for i, block in enumerate(num_32):
        decimal_value = decimal_value + block * (base ** i)
    return hex(decimal_value).lstrip("0x") or "0"

C = LongNumOperations()
print('Сума чисел А + В дорівнює:', from32_to16(C.long_add(a, b)))
print('Різниця чисел А - В дорівнює:', from32_to16(C.long_sub(a, b)))
print('Добуток чисел А х В дорівнює:', from32_to16(C.long_mul(a, b)))
#print('Ділення чисел А / В дорівнює:', from32_to16(C.long_div_mod(a, c)))

#ПЕРЕВІРКА
#print('(a + b) * c =', from32_to16(C.long_mul(C.long_add(a, b), c)))
#print('c * (a + b) =', from32_to16(C.long_mul(c, C.long_add(a, b))))
#print('a * c + b * c = ', from32_to16(C.long_add(C.long_mul(a, c), C.long_mul(b, c))))
#print('n * a = ', from32_to16(C.long_mul_one_digit(a, 100)))

"""X = [1, 2, 4, 8, 16, 32, 64, 128, 256]
y1 = [1.9*10**(-5), 1.45*10**(-5), 1.4*10**(-5), 1.5*10**(-5), 1.6*10**(-5), 1.9*10**(-5), 2*10**(-5), 2.6*10**(-5), 3.4*10**(-5)]
y2 = [7.3*10**(-6), 6.7*10**(-6), 7*10**(-6), 7*10**(-6), 8.2*10**(-6), 9.2*10**(-6), 1.1*10**(-5), 1.9*10**(-5), 2.1*10**(-5)]
y3 = [1.6*10**(-5), 1.42*10**(-5), 1.4*10**(-5), 2.2*10**(-5), 2.8*10**(-5), 5.5*10**(-5), 1.5*10**(-4), 4.7*10**(-4), 1.7*10**(-3)]
plt.plot(X, y1, color='red', label='Операція додавання')
plt.plot(X, y2, color='orange', label='Операція віднімання')
plt.plot(X, y3, color='green', label='Операція множення')
plt.title("Час виконання операцій багаторозрядної арифметики")
plt.xlabel('Довжина чисел')
plt.ylabel("Час виконання операцій")
plt.legend()
plt.show()"""

#a = "0x" + str(input("Введіть значення А: "))
#b = "0x" + str(input("Введіть значення В: "))
#c = "0x" + str(input("Введіть значення C: "))
#n = "0x" + str(input("Введіть значення N: "))

#a = "0xe4bd0c7683f8ddd24f608e02c99433cef80878d2a3d7405c57e8bfc8280c891cbbe58f63c33703f307ba410696025250c3fc9123b33d0b60145558a1008852384479dc0b800895e932ff558b576881d295b24adad789a86eaf702036c5c805895dfc8fe4712a7f5b5caae8ff780af6599dba8fb1d83ca93891ceacc5fe88dd8d6977ac2cb81ad3b88873237698455952aa7c60a4b35f53d1f0a3f264a95bbda78ccd16bd41bf9fddd7b79a828ca93295229f59103ae7a6f1daf09b411adee2449ef66a3875c076f976f7abd66a363286983f36c9156962132ab789c448a80b15386bfc0ec4836b269f0ec400e299c914ff0ac047bfcf682916341cf04f49e194"
#b = "0x727cc4fdd061512f0436c586e227fe287adbcbc426ccc83d570f2b028bdd49ee8c2754bfe2e395ee03d35fa516bef5573aa199b9ba1bcf59b607d6023f1d676863dd926c49f677a7b229697a6f779c08a05d45333723a0ff555a1f39da6116ae0c4f4eb33014fdcdb1807097d6f68043de986cb8318e3d6fbe858c57d9d6370657048d986d60ebb94cbad96207fc6dbdf222b1c8352a9e9e7bce15d96f7e0794784de4b5c27cda73c7ae30c71d1c8c78a22fdec32bd62019855482101b44eeda3142e55346f82cfd9dcef3be5ef8d41d3df8fa542a64561ffa561d572b8fdf745e3f6384e3610bfd8fd8dbcc53abfb3dff6a5ae050789f1fff54e8ee34e60950"
#c = "0xccaba6d19f3f73d114292ec3eb4a41fdc16a899158b8945526a2e88bb43b10471c5a8a3494baa734d4947800a621462c3fafe87a89d81f17335d6766c43edeca7564073740c4fec217a2007586ba9c617427e9a4c28889eb9e6cfca6b1640bd25142f9058b61e1930122ffe5309aea30ce1e6fc738510ccaab79ba18fc20b544"

a = '0x28a895cfd0200f098e2effaf19391c4a837ff199610c9bd4241b1a226effbc0ba1e4c9f81cd703a4212c02f96767adbc1e336b9d2cc5eccc98bd202bddc8fa5011f2df252fbb1843b3422db8f63129bad292c3b42a2402cf732500d8f0954fdc329c8a197a41fd984ca46b69caa59553ba92bacac9646d1a9c4508c3111f7ebf'
b = '0x20736a58fe16964aa40fbafbcb63175b370f70823dd4212ff42bfbc778478b757e15cb8f9eb1bc33ae07f2366f07c6bade3f8cb1745bd0622073c835d9ed17b9897730a542ab333ec3f25e91a36787064d30eb8c5a396d5345f580b8104249d9d90cf6a85a2ce2e09a2ef2df9308cc0c9f57ff7727e6b0f56294dafff4c3b994'
c = '0x2dc02054ff689a01dc9b1ad05270aa78a271b0c9bf058834f55843a616f85232421f0ce4a84eac70a626ecaa949f174ef2b436a4142e1dcf790dfd232a613e9a'
n = '0x2dc02054ff689a01dc9b1ad05270aa78a271b0c9bf058834f55843a616f85232421f0ce4a84eac70a626ecaa949f174ef2b436a4142e1dcf790dfd232a613e9a'


def hex_to_32(hex_num, base=2**32):
    n = int(hex_num, 16)
    blocks = []
    while n > 0:
        blocks.append(n % base)
        n = n // base
    return blocks

a = hex_to_32(a)
b = hex_to_32(b)
c = hex_to_32(c)
n = hex_to_32(n)


class LongNumOperations():
    def long_add(self, num1, num2, base=2**32):
        n = max(len(num1), len(num2))
        if len(num1) > len(num2):
            num2 = num2 + [0] * abs(len(num1) - len(num2))
        if len(num1) < len(num2):
            num1 = num1 + [0] * abs(len(num1) - len(num2))
        C = []
        carry = 0
        for i in range(n):
            temp = num1[i] + num2[i] + carry
            C.append(temp % base)
            carry = temp // base
        C.append(carry)
        return C

    def long_sub(self, num1, num2, base=2**32):
        n = max(len(num1), len(num2))
        if len(num1) > len(num2):
            num2 = num2 + [0] * abs(len(num1) - len(num2))
        if len(num1) < len(num2):
            num1 = num1 + [0] * abs(len(num1) - len(num2))
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
        n = min(len(num1), len(num2))
        C = []
        for i in range(n):
            temp = self.long_mul_one_digit(num1, num2[i])
            temp = [0] * i + temp
            C = self.long_add(C, temp)
        return C

    def normalize(self, num):
        while len(num) > 1 and num[-1] == 0:
            num.pop()
        return num

    def long_cmp(self, num1, num2):
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

    def bit_length(self, num):
        n = 32 * (len(num) - 1) + num[-1].bit_length()
        return n

    def long_div_mod(self, num1, num2):
        k = self.bit_length(num2)
        R = num1
        Q = [0] * len(num1)
        while self.long_cmp(R, num2) >= 0:
            t = self.bit_length(R)
            C = self.long_shift_bits_to_high(num2, t - k)
            if self.long_cmp(R, C) < 0:
                t = t - 1
                C = self.long_shift_bits_to_high(num2, t - k)
            R = self.long_sub(R, C)
            Q[(t - k) // 32] |= 1 << ((t - k) % 32)
        return Q, R

    def long_shift_bits_to_high(self, num, shift, base=2**32):
        if shift == 0:
            return num
        num_blocks = shift // 32
        bit_shift = shift % 32
        result = [0] * num_blocks
        carry = 0
        for block in num:
            new_block = (block << bit_shift | carry) & (base - 1)
            carry = block >> (32 - bit_shift)
            result.append(new_block)
        if carry:
            result.append(carry)
        return result

    def gcd(self, num1, num2):
        d = [1]
        while num1[0] % 2 == 0 and num2[0] % 2 == 0:
            num1 = self.shift_right(num1)
            num2 = self.shift_right(num2)
            d = self.long_mul_one_digit(d, 2)
        while num1[0] % 2 == 0:
            num1 = self.shift_right(num1)
        while num2[0] % 2 == 0:
            num2 = self.shift_right(num2)
        while num2 != [0]:
            while num2[0] % 2 == 0:
                num2 = self.shift_right(num2)
            if self.long_cmp(num1, num2) > 0:
                num1, num2 = num2, self.long_sub(num1, num2)
            else:
                num1, num2 = num1, self.long_sub(num2, num1)
        d = self.long_mul(num1, d)
        return self.normalize(d)

    def shift_right(self, num):
        carry = 0
        for i in range(len(num) - 1, -1, -1):
            current = (carry << 32) | num[i]
            num[i] = current >> 1
            carry = current & 1
        while len(num) > 1 and num[-1] == 0:
            num.pop()
        return num

    def lcm(self, num1, num2):
        a = self.long_mul(num1, num2)
        b = self.gcd(num1, num2)
        m, r = self.long_div_mod(a, b)
        return m

    def kill_last_digits(self, num, k):
        if k < len(num):
            num = num[k:]
        else:
            num = [0]
        return num

    def predict_mu(self, n, k):
        base_2k = [0] * (2 * k) + [1]
        mu, r = self.long_div_mod(base_2k, n)
        return mu

    def barrett_reduction(self, x, n, mu):
        k = len(n)
        q = self.kill_last_digits(x, k - 1)
        q = self.long_mul(q, mu)
        q = self.kill_last_digits(q, k + 1)
        r = self.long_sub(x, self.long_mul(q, n))
        while self.long_cmp(r, n) >= 0:
            r = self.long_sub(r, n)
        return r

    def base_2_32_to_binary(self, blocks):
        binary_str = ''.join(f'{block:032b}' for block in reversed(blocks))
        return binary_str.lstrip('0') or '0'

    def long_mod_add(self, num1, num2, n):
        k = len(n)
        mu = self.predict_mu(n, k)
        num1 = self.barrett_reduction(num1, n, mu)
        num2 = self.barrett_reduction(num2, n, mu)
        result = self.barrett_reduction(self.long_add(num1, num2), n, mu)
        return result

    def long_mod_sub(self, num1, num2, n):
        k = len(n)
        mu = self.predict_mu(n, k)
        result = self.barrett_reduction(self.long_sub(num1, num2), n, mu)
        return result

    def long_mod_power_2(self, num, n, mu=None):
        if mu is None:
            k = len(n)
            mu = self.predict_mu(n, k)
            num = self.barrett_reduction(num, n, mu)
            num = self.barrett_reduction(self.long_mul(num, num), n, mu)
        else:
            num = self.barrett_reduction(num, n, mu)
            num = self.barrett_reduction(self.long_mul(num, num), n, mu)
        return num

    def long_mod_mul(self, num1, num2, n, mu=None):
        if mu is None:
            k = len(n)
            mu = self.predict_mu(n, k)
            num1 = self.barrett_reduction(num1, n, mu)
            num2 = self.barrett_reduction(num2, n, mu)
            result = self.barrett_reduction(self.long_mul(num1, num2), n, mu)
        else:
            num1 = self.barrett_reduction(num1, n, mu)
            num2 = self.barrett_reduction(num2, n, mu)
            result = self.barrett_reduction(self.long_mul(num1, num2), n, mu)
        return result

    def long_mod_power_barret(self, num1, num2, n):
        C = [1]
        k = len(n)
        mu = self.predict_mu(n, k)
        # num1 = self.barrett_reduction(num1, n, mu)
        num2 = self.base_2_32_to_binary(num2)
        for i in range(len(num2)):
            if num2[i] == '1':
                C = self.long_mod_mul(C, num1, n, mu)
            num1 = self.long_mod_power_2(num1, n, mu)
        return C


def from32_to16(num_32, base=2**32):
    decimal_value = 0
    for i, block in enumerate(num_32):
        decimal_value = decimal_value + block * (base ** i)
    return hex(decimal_value).lstrip("0x") or "0"


C = LongNumOperations()
print('Сума чисел А + В дорівнює:', from32_to16(C.long_add(a, b)))
print('Різниця чисел А - В дорівнює:', from32_to16(C.long_sub(a, b)))
print('Добуток чисел А х В дорівнює:', from32_to16(C.long_mul(a, b)))
Q, R = C.long_div_mod(a, c)
print('Ціла частка від ділення чисел А / C дорівнює:', from32_to16(Q))
print('Залишок від ділення чисел А / C дорівнює:', from32_to16(R))
print('Сума чисел А + В за модулем N дорівнює:', from32_to16(C.long_mod_add(a, b, n)))
print('Різниця чисел А - В за модулем N дорівнює:', from32_to16(C.long_mod_sub(a, b, n)))
print('Добуток чисел А х В за модулем N дорівнює:', from32_to16(C.long_mod_mul(a, b, n)))
print('Квадрат числа А за модулем N дорівнює:', from32_to16(C.long_mod_power_2(a, n)))
print('Power Barrett:', from32_to16(C.long_mod_power_barret(a, b, c)))
print('Найменше спільне кратне чисел А і В дорівнює:', from32_to16(C.lcm(a, b)))
print('Найбільший спільний дільник чисел А і В дорівнює:', from32_to16(C.gcd(a, b)))


#ПЕРЕВІРКА_1
#print('(a + b) * c =', from32_to16(C.long_mul(C.long_add(a, b), c)))
#print('c * (a + b) =', from32_to16(C.long_mul(c, C.long_add(a, b))))
#print('a * c + b * c = ', from32_to16(C.long_add(C.long_mul(a, c), C.long_mul(b, c))))
#print('n * a = ', from32_to16(C.long_mul_one_digit(a, 100)))

"""X = [1, 2, 4, 8, 16, 32, 64, 128, 256]
y1 = [1.9*10**(-5), 1.45*10**(-5), 1.4*10**(-5), 1.5*10**(-5), 1.6*10**(-5), 1.9*10**(-5), 2*10**(-5), 2.6*10**(-5), 3.4*10**(-5)]
y2 = [7.3*10**(-6), 6.7*10**(-6), 7*10**(-6), 7*10**(-6), 8.2*10**(-6), 9.2*10**(-6), 1.1*10**(-5), 1.9*10**(-5), 2.1*10**(-5)]
y3 = [1.6*10**(-5), 1.42*10**(-5), 1.4*10**(-5), 2.2*10**(-5), 2.8*10**(-5), 5.5*10**(-5), 1.5*10**(-4), 4.7*10**(-4), 1.7*10**(-3)]
y4 = [3.2*10**(-5), 4.8*10**(-5), 9.1*10**(-5), 9.9*10**(-5), 2.7*10**(-4), 5.8*10**(-4), 1.2*10**(-3), 3.1*10**(-3), 9.4*10**(-3)]
plt.plot(X, y1, color='red', label='Операція додавання')
plt.plot(X, y2, color='orange', label='Операція віднімання')
plt.plot(X, y3, color='green', label='Операція множення')
plt.plot(X, y4, color='blue', label='Операція ділення')
plt.title("Час виконання операцій багаторозрядної арифметики")
plt.xlabel('Довжина чисел')
plt.ylabel("Час виконання операцій")
plt.legend()
plt.show()"""

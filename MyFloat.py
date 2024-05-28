import math

class MyFloat:
    def __init__(self, beta, t, L, U, value):
        self.beta = beta
        self.t = t
        self.L = L
        self.U = U
        self.value = [0] * t
        self.exponent = 0
        self.sign = 0

        if(value < 0):
            self.sign = -1
            value = -value
        else:
            self.sign = 1

        intV, decV = divmod(value, 1)
        digits = 0
        decimals = 0

        if(intV > 0):
            digits = min(t - 1, int(math.log(intV, beta)) + 1)
            for i in range(digits - 1, -1, -1):
                self.value[i] = int(intV % beta)
                intV //= beta

        if(decV > 0):

            while(int(decV * beta) == 0):
                decV *= beta
                decimals -= 1

            for i in range(digits, t):
                decV *= beta
                self.value[i] = int(decV)
                decV -= int(decV) * 1.0

        self.exponent = digits if digits > 0 else decimals
        
        if(not self.check()):
            raise ValueError("Invalid MyFloat")

    def check(self):
        for i in range(self.t):
            if(self.value[i] < 0 or self.value[i] >= self.beta):
                return False
        if(self.sign == 0):
            return False   
        if(self.exponent < self.L or self.exponent > self.U):
            return False
        return True
    
    def normalize(self):
        # Remove leading zeros and adjust the exponent accordingly
        i = 0
        while i < self.t and self.value[i] == 0:
            i += 1
        if i == self.t:  # All zeros
            self.exponent = 0
            self.sign = 1
        else:
            shift = i
            self.value = self.value[shift:] + [0] * shift
            self.exponent -= shift
            
    def __add__(self, other):
        if self.beta != other.beta or self.t != other.t:
            raise ValueError("Cannot add MyFloat objects with different bases or precision")

        if self.sign == 0:
            return other
        if other.sign == 0:
            return self

        result = MyFloat(self.beta, self.t, self.L, self.U, 0.0)
        if self.exponent > other.exponent:
            shift = self.exponent - other.exponent
            larger = self
            smaller = other
        else:
            shift = other.exponent - self.exponent
            larger = other
            smaller = self

        result.exponent = max(self.exponent, other.exponent)
        carry = 0
        for i in range(self.t - 1, -1, -1):
            if i - shift >= 0:
                sum_value = larger.value[i] + smaller.value[i - shift] + carry
            else:
                sum_value = larger.value[i] + carry

            carry = sum_value // self.beta
            result.value[i] = sum_value % self.beta

        if carry > 0:
            raise ValueError("Overflow in addition")

        result.normalize()
        return result

    def __sub__(self, other):
        if self.beta != other.beta or self.t != other.t:
            raise ValueError("Cannot subtract MyFloat objects with different bases or precision")

        if self.sign == 0:
            return MyFloat(self.beta, self.t, self.L, self.U, -other)

        result = MyFloat(self.beta, self.t, self.L, self.U, 0.0)
        if self.exponent > other.exponent:
            shift = self.exponent - other.exponent
            larger = self
            smaller = other
        else:
            shift = other.exponent - self.exponent
            larger = other
            smaller = self

        if self < other:
            larger, smaller = smaller, larger
            result.sign = -1
        else:
            result.sign = 1

        result.exponent = max(self.exponent, other.exponent)
        borrow = 0
        for i in range(self.t - 1, -1, -1):
            if i - shift >= 0:
                sub_value = larger.value[i] - smaller.value[i - shift] - borrow
            else:
                sub_value = larger.value[i] - borrow

            if sub_value < 0:
                sub_value += self.beta
                borrow = 1
            else:
                borrow = 0

            result.value[i] = sub_value

        result.normalize()
        return result
    
    def __lt__(self, other):
        if self.exponent != other.exponent:
            return self.exponent < other.exponent
        return self.value < other.value

    def __repr__(self):
        return f"MyFloat(beta={self.beta}, t={self.t}, L={self.L}, U={self.U}, value={self.value}, exponent={self.exponent}, sign={self.sign})"
    


print(MyFloat(10, 3, -1, 1, 5.0) + MyFloat(10, 3, -1, 1, 5.0))
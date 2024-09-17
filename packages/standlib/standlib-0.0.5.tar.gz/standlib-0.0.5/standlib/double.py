class Double:

    """A class representing a double-precision floating-point number.

    Attributes:
        precision (int): The number of decimal places to maintain.
        value (str): The value of the number as a string.

    Methods:
        __init__(value, precision=None): Initializes a new Double object with the given value and precision.
        _parse(value): Parses the given value into a string representation.
        __repr__(): Returns a string representation of the Double object.
        __str__(): Returns a formatted string representation of the Double object.
        _format(value): Formats the given value to the specified precision.
        __add__(other): Adds the given value to this Double object.
        __sub__(other): Subtracts the given value from this Double object.
        __mul__(other): Multiplies this Double object by the given value.
        __truediv__(other): Divides this Double object by the given value.
        _add(a, b): Adds two string representations of numbers.
        _subtract(a, b): Subtracts two string representations of numbers.
        _multiply(a, b): Multiplies two string representations of numbers.
        _divide(a, b): Divides two string representations of numbers.
        set_default_precision(precision): Sets the default precision for all Double objects.
        get_default_precision(): Gets the default precision for all Double objects.
    """

    default_precision = 50  

    def __init__(self, value, precision=None) -> None:
        self.precision = precision if precision is not None else Double.default_precision
        self.value = self._parse(value)

    """Initializes a new Double object.

        Args:
            value (int, float, or str): The initial value of the Double object.
            precision (int, optional): The number of decimal places to maintain. Defaults to the default_precision class attribute.
        """
    
    def _parse(self, value):
        if isinstance(value, (int, float)):
            value = str(value)
        elif not isinstance(value, str):
            raise TypeError("Value must be an int, float, or str")
        
        if '.' in value:
            integer_part, decimal_part = value.split('.')
        else:
            integer_part, decimal_part = value, ''
        
        integer_part = integer_part.lstrip('0') or '0'
        decimal_part = decimal_part.rstrip('0')
        
        
        if not decimal_part:
            decimal_part = '0'
        
        return f"{integer_part}.{decimal_part}"

    def __repr__(self) :
        return f"Double({self._format(value=self.value)})"
    
    def __str__(self):
        return self._format(self.value)

    def _format(self, value: str):

        """Formats the given value to the specified precision.

        Args:
            value (str): The value to format.

        Returns:
            str: The formatted value.
        """

        integer_part, decimal_part = value.split('.')
        if len(decimal_part) < self.precision:
            return f"{integer_part}.{decimal_part.ljust(self.precision, '0')}"
        else:
            return f"{integer_part}.{decimal_part[:self.precision]}"

    def __add__(self, other) -> "Double":
        
        """Adds the given value to this Double object.

        Args:
            other (Double, int, or float): The value to add.

        Returns:
            Double: The result of the addition.

        Raises:
            TypeError: If the other operand is not a Double, int, or float.
        """

        if isinstance(other, (Double, int, float)):
            if not isinstance(other, Double):
                other = Double(other, self.precision)
            result = self._add(self.value, other.value)
            return Double(result, self.precision)
        raise TypeError("Operands must be of type Double, int, or float")

    def __sub__(self, other) -> "Double":

        """Subtracts the given value from this Double object.

        Args:
            other (Double, int, or float): The value to subtract.

        Returns:
            Double: The result of the subtraction.

        Raises:
            TypeError: If the other operand is not a Double, int, or float.
        """

        if isinstance(other, (Double, int, float)):
            if not isinstance(other, Double):
                other = Double(other, self.precision)
            result = self._subtract(self.value, other.value)
            return Double(result, self.precision)
        raise TypeError("Operands must be of type Double, int, or float")

    def __mul__(self, other) -> "Double":

        """Multiplies this Double object by the given value.

        Args:
            other (Double, int, or float): The value to multiply by.

        Returns:
            Double: The result of the multiplication.

        Raises:
            TypeError: If the other operand is not a Double, int, or float.
        """

        if isinstance(other, (Double, int, float)):
            if not isinstance(other, Double):
                other = Double(other, self.precision)
            result = self._multiply(self.value, other.value)
            return Double(result, self.precision)
        raise TypeError("Operands must be of type Double, int, or float")

    def __truediv__(self, other) -> "Double":

        """Divides this Double object by the given value.

        Args:
            other (Double, int, or float): The value to divide by.

        Returns:
            Double: The result of the division.

        Raises:
            TypeError: If the other operand is not a Double, int, or float.
            ZeroDivisionError: If the divisor is zero.
        """

        if isinstance(other, (Double, int, float)):
            if not isinstance(other, Double):
                other = Double(other, self.precision)
            if other.value == '0.0':
                raise ZeroDivisionError("Division by zero")
            result = self._divide(self.value, other.value)
            return Double(result, self.precision)
        raise TypeError("Operands must be of type Double, int, or float")

    def _add(self, a: str, b: str) -> str:

        """Adds two string representations of numbers.

        Args:
            a (str): The first number.
            b (str): The second number.

        Returns:
            str: The sum of the two numbers.
            """

        a_int, a_dec = a.split('.')
        b_int, b_dec = b.split('.')
        
        max_dec_len = max(len(a_dec), len(b_dec))
        a_dec = a_dec.ljust(max_dec_len, '0')
        b_dec = b_dec.ljust(max_dec_len, '0')
        
        int_sum = int(a_int) + int(b_int)
        dec_sum = int(a_dec) + int(b_dec)
        
        if len(str(dec_sum)) > max_dec_len:
            int_sum += dec_sum // (10 ** max_dec_len)
            dec_sum = dec_sum % (10 ** max_dec_len)
        
        return f"{int_sum}.{str(dec_sum).zfill(max_dec_len)}"

    def _subtract(self, a: str, b: str) -> str:

        """Subtracts two string representations of numbers.

        Args:
            a (str): The minuend.
            b (str): The subtrahend.

        Returns:
            str: The difference of the two numbers.
        """

        a_int, a_dec = a.split('.')
        b_int, b_dec = b.split('.')
        
        max_dec_len = max(len(a_dec), len(b_dec))
        a_dec = a_dec.ljust(max_dec_len, '0')
        b_dec = b_dec.ljust(max_dec_len, '0')
        
        int_diff = int(a_int) - int(b_int)
        dec_diff = int(a_dec) - int(b_dec)
        
        if dec_diff < 0:
            int_diff -= 1
            dec_diff += 10 ** max_dec_len
        
        return f"{int_diff}.{str(dec_diff).zfill(max_dec_len)}"

    def _multiply(self, a: str, b: str) -> str:

        """Multiplies two string representations of numbers.

        Args:
            a (str): The first factor.
            b (str): The second factor.

        Returns:
            str: The product of the two numbers.
        """

        a_int, a_dec = a.split('.')
        b_int, b_dec = b.split('.')
        
        int_product = int(a_int) * int(b_int)
        dec_product = int(a_dec) * int(b_dec)
        
        return f"{int_product}.{str(dec_product).ljust(self.precision, '0')}"

    def _divide(self, a: str, b: str) -> str:

        """Divides two string representations of numbers.

        Args:
            a (str): The dividend.
            b (str): The divisor.

        Returns:
            str: The quotient of the two numbers.
        """

        a_int, a_dec = a.split('.')
        b_int, b_dec = b.split('.')
        
        int_div = int(a_int) // int(b_int)
        dec_div = int(a_dec) // int(b_dec)
        
        return f"{int_div}.{str(dec_div).ljust(self.precision, '0')}"

    @classmethod
    def set_default_precision(cls, precision: int) -> None:

        """Sets the default precision for all Double objects.

        Args:
            precision (int): The new default precision.
        """

        cls.default_precision = precision

    @classmethod
    def get_default_precision(cls) -> int:

        """Gets the default precision for all Double objects.

        Returns:
            int: The current default precision.
        """

        return cls.default_precision

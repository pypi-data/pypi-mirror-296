# arithmetic_lib/arithmetic.py

class Arithmetic:
    @staticmethod
    def add(a, b):
        """Returns the sum of a and b."""
        return a + b

    @staticmethod
    def subtract(a, b):
        """Returns the difference between a and b."""
        return a - b

    @staticmethod
    def multiply(a, b):
        """Returns the product of a and b."""
        return a * b

    @staticmethod
    def divide(a, b):
        """Returns the division of a by b. Raises an error if dividing by zero."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    @staticmethod
    def modulus(a, b):
        """Returns the modulus of a and b."""
        return a % b

    @staticmethod
    def power(a, b):
        """Returns a raised to the power of b."""
        return a ** b

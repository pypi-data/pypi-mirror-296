import math

__version__ = "2.1.2" 

def fibonacci(iter=10):
    """Devuelve una lista con los primeros 'iter' números de la serie de Fibonacci."""
    try:
        if iter < 0:
            raise ValueError("El número de iteraciones no puede ser negativo.")
        sequence = []
        a, b = 0, 1
        for _ in range(iter):
            sequence.append(b)
            a, b = b, a + b
        return sequence
    except TypeError:
        raise TypeError("El argumento 'iter' debe ser un entero.")

def fibonacci_generator():
    """Generador que produce los números de la serie de Fibonacci de manera indefinida."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def is_perfect_square(x):
    """Verifica si un número es un cuadrado perfecto."""
    try:
        if x < 0:
            raise ValueError("El número no puede ser negativo.")
        s = int(math.sqrt(x))
        return s * s == x
    except TypeError:
        raise TypeError("El argumento 'x' debe ser un número.")

def is_fibonacci(n):
    """Devuelve True si el número 'n' es un número de Fibonacci, False en caso contrario."""
    try:
        if n < 0:
            raise ValueError("El número no puede ser negativo.")
        return is_perfect_square(5 * n * n + 4) or is_perfect_square(5 * n * n - 4)
    except TypeError:
        raise TypeError("El argumento 'n' debe ser un número entero.")

def fibonacci_n(n):
    """Devuelve el n-ésimo número de Fibonacci."""
    try:
        if n < 0:
            raise ValueError("El número no puede ser negativo.")
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a
    except TypeError:
        raise TypeError("El argumento 'n' debe ser un número entero.")

def fibonacci_sum(n):
    """Devuelve la suma de los primeros 'n' números de Fibonacci."""
    try:
        if n < 0:
            raise ValueError("El número no puede ser negativo.")
        a, b = 0, 1
        total = 0
        for _ in range(n):
            total += a
            a, b = b, a + b
        return total
    except TypeError:
        raise TypeError("El argumento 'n' debe ser un número entero.")

def fibonacci_less_than(n):
    """Devuelve una lista con todos los números de Fibonacci menores que 'n'."""
    try:
        if n < 0:
            raise ValueError("El número no puede ser negativo.")
        result = []
        a, b = 0, 1
        while a < n:
            result.append(a)
            a, b = b, a + b
        return result
    except TypeError:
        raise TypeError("El argumento 'n' debe ser un número.")

def golden_ratio(n):
    """Calcula la aproximación de la razón dorada usando los dos últimos 'n' términos de Fibonacci."""
    try:
        if n <= 0:
            raise ValueError("El número debe ser mayor que cero.")
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return b / a if a != 0 else None
    except TypeError:
        raise TypeError("El argumento 'n' debe ser un número entero.")

def fibonacci_remainder(n, m):
    """Devuelve una lista con los primeros 'n' números de Fibonacci resto 'm'."""
    try:
        if n < 0 or m <= 0:
            raise ValueError("'n' no puede ser negativo y 'm' debe ser mayor que cero.")
        sequence = []
        a, b = 0, 1
        for _ in range(n):
            sequence.append(a % m)
            a, b = b, a + b
        return sequence
    except TypeError:
        raise TypeError("Los argumentos 'n' y 'm' deben ser números enteros.")

def is_divisible_by_fibonacci(n, return_divisors=False):
    """
    Devuelve True si 'n' es divisible por algún número de Fibonacci mayor que 1.
    Si 'return_divisors' es True, devuelve la lista de los números de Fibonacci que dividen a 'n'.
    """
    try:
        if n <= 0:
            raise ValueError("El número debe ser mayor que cero.")
        a, b = 0, 1
        divisors = []  # Para almacenar los divisores si se solicita
        
        while a <= n:
            if a > 1 and n % a == 0:  # Excluye 0 y 1
                if return_divisors:
                    divisors.append(a)  # Guarda el divisor
                else:
                    return True  # Si no se necesita la lista, devuelve True inmediatamente
            a, b = b, a + b
        
        # Si se solicita la lista de divisores
        if return_divisors:
            return divisors
        else:
            return False
    except TypeError:
        raise TypeError("El argumento 'n' debe ser un número entero.")

def custom_fibonacci(n, first=0, second=1):
    """Genera los primeros 'n' números de una secuencia de Fibonacci personalizada."""
    try:
        if n < 0:
            raise ValueError("El número 'n' no puede ser negativo.")
        sequence = []
        a, b = first, second
        for _ in range(n):
            sequence.append(a)
            a, b = b, a + b
        return sequence
    except TypeError:
        raise TypeError("Los argumentos 'n', 'first' y 'second' deben ser números enteros.")


def help():
    """Muestra la lista de funciones disponibles y sus descripciones."""
    print("""
    Funciones disponibles en pynacci.py:
    
    1. fibonacci(iter=10): Devuelve una lista con los primeros 'iter' números de la serie de Fibonacci.
    
    2. fibonacci_generator(): Generador que produce los números de la serie de Fibonacci de manera indefinida.
    
    3. is_perfect_square(x): Verifica si un número es un cuadrado perfecto.
    
    4. is_fibonacci(n): Devuelve True si el número 'n' es un número de Fibonacci, False en caso contrario.
    
    5. fibonacci_n(n): Devuelve el n-ésimo número de Fibonacci.
    
    6. fibonacci_sum(n): Devuelve la suma de los primeros 'n' números de Fibonacci.
    
    7. fibonacci_less_than(n): Devuelve una lista con todos los números de Fibonacci menores que 'n'.
    
    8. golden_ratio(n): Calcula la aproximación de la razón dorada usando los dos últimos 'n' términos de Fibonacci.
    
    9. fibonacci_remainder(n, m): Devuelve una lista con los primeros 'n' números de Fibonacci resto 'm'.
    
    10. is_divisible_by_fibonacci(n, return_divisors=False): 
        Devuelve True si 'n' es divisible por algún número de Fibonacci mayor que 1.
        Si 'return_divisors' es True, devuelve la lista de los números de Fibonacci que dividen a 'n'.
    
    11. custom_fibonacci(n, first=0, second=1): 
        Genera los primeros 'n' números de una secuencia de Fibonacci personalizada.
    
    """)


__all__ = ['fibonacci', 'fibonacci_generator', 'is_perfect_square', 'is_fibonacci', 'fibonacci_n', 'fibonacci_sum',
           'fibonacci_less_than', 'golden_ratio', 'fibonacci_remainder', 'is_divisible_by_fibonacci', 'custom_fibonacci', 'help']

# pynacci.py

import math

__version__ = "2.0.0" 

def fibonacci(iter=10):
    """Devuelve una lista con los primeros 'iter' números de la serie de Fibonacci."""
    sequence = []
    a, b = 0, 1
    for _ in range(iter):
        sequence.append(b)
        a, b = b, a + b
    return sequence

def fibonacci_generator():
    """Generador que produce los números de la serie de Fibonacci de manera indefinida."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def is_perfect_square(x):
    """Verifica si un número es un cuadrado perfecto."""
    s = int(math.sqrt(x))
    return s * s == x

def is_fibonacci(n):
    """Devuelve True si el número 'n' es un número de Fibonacci, False en caso contrario."""
    return is_perfect_square(5 * n * n + 4) or is_perfect_square(5 * n * n - 4)

def fibonacci_n(n):
    """Devuelve el n-ésimo número de Fibonacci."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def fibonacci_sum(n):
    """Devuelve la suma de los primeros 'n' números de Fibonacci."""
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

def fibonacci_less_than(n):
    """Devuelve una lista con todos los números de Fibonacci menores que 'n'."""
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a + b
    return result

def golden_ratio(n):
    """Calcula la aproximación de la razón dorada usando los primeros 'n' términos de Fibonacci."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return b / a if a != 0 else None 

def fibonacci_mod(n, m):
    """Devuelve una lista con los primeros 'n' números de Fibonacci módulo 'm'."""
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a % m)
        a, b = b, a + b
    return sequence

def is_divisible_by_fibonacci(n):
    """Devuelve True si 'n' es divisible por algún número de Fibonacci."""
    a, b = 0, 1
    while a <= n:
        if a != 0 and n % a == 0:
            return True
        a, b = b, a + b
    return False

def custom_fibonacci(n, first=0, second=1):
    """Genera los primeros 'n' números de una secuencia de Fibonacci personalizada."""
    sequence = []
    a, b = first, second
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence


__all__ = ['fibonacci', 'fibonacci_generator', 'is_perfect_square', 'is_fibonacci', 'fibonacci_n', 'fibonacci_sum',
           'fibonacci_less_than', 'golden_ratio', 'fibonacci_mod', 'is_divisible_by_fibonacci', 'custom_fibonacci']

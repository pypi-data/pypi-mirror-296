# pynacci.py

__version__ = "1.1.0"

def is_in_fibonacci(number):
    """Devuelve True si el número está en la serie de Fibonacci, False si no."""
    a, b = 0, 1
    while b <= number:
        if b == number:
            return True
        a, b = b, a + b
    return False

def fibonacci(iter):
    """Devuelve una lista con los primeros 'iter' números de la serie de Fibonacci."""
    sequence = []
    a, b = 0, 1
    for _ in range(iter):
        sequence.append(b)
        a, b = b, a + b
    return sequence

def fibonacci_generator():
    """Generador que produce números de la secuencia de Fibonacci."""
    a, b = 0, 1
    while True:
        yield b
        a, b = b, a + b

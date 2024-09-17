# pynacci.py

__version__ = "1.1.2"  

def fibonacci(iter = 10):
    """Devuelve una lista con los primeros 'iter' números de la serie de Fibonacci."""
    sequence = []
    a, b = 0, 1
    for _ in range(iter):
        sequence.append(b)
        a, b = b, a + b
    return sequence

__all__ = ['fibonacci']

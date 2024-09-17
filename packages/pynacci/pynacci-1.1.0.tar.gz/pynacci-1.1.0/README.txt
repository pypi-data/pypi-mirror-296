# README.txt

pynacci
=======

Una librería de Python para trabajar con la serie de Fibonacci.

## Instalación

Puedes instalar la librería utilizando `pip`:

pip install pynacci


## Uso

```python
import pynacci

# Obtener los primeros 10 números de Fibonacci
print(pynacci.fibonacci(10))

# Verificar si un número está en la serie de Fibonacci
print(pynacci.is_in_fibonacci(21))  # Devolverá True
print(pynacci.is_in_fibonacci(22))  # Devolverá False

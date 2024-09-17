# pynacci/pynacci/fibonacci.py

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

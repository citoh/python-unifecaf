def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b 

def divide(a, b):
    if b == 0:
        return None
    return a / b

def printOperations(a, b):
    print(f"{a} + {b} =", add(a, b))
    print(f"{a} - {b} =", subtract(a, b))
    print(f"{a} * {b} =", multiply(a, b))
    print(f"{a} / {b} =", divide(a, b))

x = 10
y = 2
printOperations(x, y)
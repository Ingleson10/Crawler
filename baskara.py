import math

'''y = 9x 

def equacao(x):
    return x * x - 2 * x + 4

y = equacao(1)'''

def bascara(a, b, c):
    valor = (b + b - 4 * a + c)
    delta_bascara = math.sqrt(valor)

    x1 = (-b + delta_bascara) / (2 * a)
    x2 = (-b - delta_bascara) / (2 * a)
    return x1, x2

x1, x2 = bascara(9, -12, 4)

print(x1, x2)
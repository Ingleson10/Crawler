'''n = 1000
palavra = 'banana'
palavra2 = '1000'
n2 = True

if 10 + 10 == 20:
    print('foi')'''



def soma(x, y):
   return x + y

def multiplicao(x, y):
   return x * y

def subtracao(x , y):
   return x - y

def divisao(x, y):
   return x / y

print('Digite o número da operação')
print('1. Somar: ')
print('2. Multiplicar: ')
print('3. Subtrair: ')
print('4. Dividir: ')
print('5. Sair do calculadora')

escolher = int(input())

x = int(input('Digite o valor de x: '))
y = int(input('Digite o valor de y: '))
resultado = 'nada foi escrito'
if escolher == 1:
    resultado = soma(x, y)

print(resultado)


'''banana = 'nanica'
n1 = 10

def soma(x, y):
    return x + y

print('O resultado da soma é:', soma(10, 20))

resultado = soma(10, 20)

if resultado > 10:
    print('oi')

def resolver_equacao(x):
    return x*x + 4 * x + 2'''

class Animal:
    nome = ''
    especie = ''
    carnivoro = False

    def __init__(self, nome, especie, carnivoro):
        self.nome = nome
        self.especie = especie
        self.carnivoro = carnivoro

    def nosso_print(self, texto):
        print(self.nome, texto)

    def comer(self):
        self.nosso_print('Comendo....')
        
    def dormir(self):
        self.nosso_print('Dormindo...')

class Passaro(Animal):
    def voar(self):
        self.nosso_print('Voando...')

class Mamifero(Animal):
    def mama(self):
        self.nosso_print('Mamando...')

class MamiferoQueNada(Mamifero):
    def nada(self):
        self.nosso_print('Nadando...')

baleia = MamiferoQueNada('Frewili', 'Cachalote', False)
baleia.nada()
baleia.comer()
baleia.mama()
baleia.dormir()
passaro = Passaro('Pindamonhagaba', 'Andorinha', False)
passaro.comer()
passaro.voar()
passaro.dormir()
leao = Mamifero('Alex', 'Leao Branco', True)
leao.comer()
leao.mama()
leao.dormir()



from cartas import Carta
import random


class Baralho(Carta):
    def __init__(self):
        self.cartas = [Carta(num, naipe) for num in [1, 2, 3, 4, 5, 6, 7, 10, 11, 12] for naipe in 'epco']

    def retorna6(self):
        self.embaralha()
        return self.cartas[:6]

    def embaralha(self):
        random.shuffle(self.cartas)

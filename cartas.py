# classe precisa ter o valor numerico da carta e o naipe

valores_carta_truco = {
    (1, 'e'): 13,
    (2, 'e'): 8,
    (3, 'e'): 9,
    (4, 'e'): 0,
    (5, 'e'): 1,
    (6, 'e'): 2,
    (7, 'e'): 11,
    (10, 'e'): 4,
    (11, 'e'): 5,
    (12, 'e'): 6,

    (1, 'p'): 12,
    (2, 'p'): 8,
    (3, 'p'): 9,
    (4, 'p'): 0,
    (5, 'p'): 1,
    (6, 'p'): 2,
    (7, 'p'): 3,
    (10, 'p'): 4,
    (11, 'p'): 5,
    (12, 'p'): 6,

    (1, 'o'): 7,
    (2, 'o'): 8,
    (3, 'o'): 9,
    (4, 'o'): 0,
    (5, 'o'): 1,
    (6, 'o'): 2,
    (7, 'o'): 10,
    (10, 'o'): 4,
    (11, 'o'): 5,
    (12, 'o'): 6,

    (1, 'c'): 7,
    (2, 'c'): 8,
    (3, 'c'): 9,
    (4, 'c'): 0,
    (5, 'c'): 1,
    (6, 'c'): 2,
    (7, 'c'): 3,
    (10, 'c'): 4,
    (11, 'c'): 5,
    (12, 'c'): 6,
}


class Carta():
    # carta -> dicionario onde as chaves sao o numero da carta,
    # e o valor é a ordem de prescedência das cartas numa disputa em ordem crescente
    def __init__(self, num, naipe):
        self.num = num
        self.naipe = naipe
        self.valor = valores_carta_truco[(num, naipe)]

    def __str__(self):
        return f"({self.naipe} - {self.num}), {self.valor}"

    def obter_numero_identificacao(self):
        naipes = ['e', 'p', 'o', 'c']
        num_carta = int(self.num)
        naipe_index = naipes.index(self.naipe)
        identificacao = (naipe_index * 10) + num_carta
        return identificacao

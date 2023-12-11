
from baralho import Baralho

import threading

import pickle
import random
import socket

HOST = "localhost"
PORT = 8080

baralho = Baralho()

estado_do_jogo = {

    "rodada": {
        "quem_comeca": 1,
        "quem_joga": 1,

        "cartas_p1": [],
        "p1_jogadas": [],
        "cartas_p2": [],
        "p2_jogadas": [],

        "pedido_envido": 0,
        "pedido_truco": 0,

        "valor_rodada": 1
    },

    "jogo": {
        "rodada": 0,

        "pontosP1": 0,
        "pontosP2": 0,
        "fim_jogo": False
    }
}


def jogador(conn, conn1, addr, id):
    global estado_do_jogo, baralho

    with conn:
        print(f"Connected by {addr}")
        conn.send(pickle.dumps([id, estado_do_jogo]))

        while True:
            data = conn.recv(1024)

            if not data:
                continue

            try:
                data = pickle.loads(data)
            except:
                print("Erro no pickle")

            rodada = estado_do_jogo['rodada']

            try:
                index = int(data['carta'])

                rodada[f'p{id}_jogadas'].append(index)

                carta_atual = rodada[f'cartas_p{id}'][index]
                cartas_jogadas = [index, carta_atual.__str__()]
            except:
                cartas_jogadas = []

            valor_rodada = 0

            pode_envido = True

            if not rodada['pedido_envido'] or rodada['pedido_truco']:
                pode_envido = False

            if data['pediu_truco']:
                print(data['pediu_truco'])
                valor_rodada = data['pediu_truco']
                estado_do_jogo['rodada']['pedido_truco'] = True
                valor_rodada = estado_do_jogo['rodada']['valor_rodada']

                if valor_rodada == 1:
                    estado_do_jogo['rodada']['valor_rodada'] = 2
                elif valor_rodada == 2:
                    estado_do_jogo['rodada']['valor_rodada'] = 3
                elif valor_rodada == 3:
                    estado_do_jogo['rodada']['valor_rodada'] = 4

            conn1.send(pickle.dumps({
                'id': id,
                'cartas_jogadas': cartas_jogadas,
                'ultima_mensagem': data['mensagem'],
                'envido': data['pediu_envido'],
                'truco': valor_rodada,
                'pode_envido': pode_envido
            }))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()

    ids = [1, 2]

    random.shuffle(ids)

    conn, addr = server.accept()
    conn1, addr1 = server.accept()
    j1 = threading.Thread(target=jogador, args=(conn, conn1, addr, ids[0]))
    j2 = threading.Thread(target=jogador, args=(conn1, conn, addr1, ids[1]))

    baralho.embaralha()

    cartas = baralho.retorna6()
    estado_do_jogo['rodada']['cartas_p1'] = cartas[3:]
    estado_do_jogo['rodada']['cartas_p2'] = cartas[:3]

    j1.start()
    j2.start()

    while not estado_do_jogo['jogo']['fim_jogo']:
        baralho.embaralha()


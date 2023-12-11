import random

import PySimpleGUI as sg

from cartas import *

import threading
from layouts import *
import pickle
import socket


id = 0

rodada = {
    'mao': [],
    'cartas_oponente': [],
    'valor_truco': 0,
    'valor_envido': 0,
    'rodada': 1
}

mostra_truco = False
mostra_envido = False

popups_truco = [pop_truco, pop_retruco, pop_valequatro]

HOST = ""
PORT = 0

path = './cartas/'
verso = './cartas/verso.png'

sg.theme('Default1')  # Add a touch of color

pontos_p1 = [[sg.Text("J1")], [sg.Text("0")]]
pontos_p2 = [[sg.Text("J2")], [sg.Text("0")]]

flor_disabled = True
conectou = False


def disable_envido(disabled, window):
    window['$EN'].update(disabled=disabled)
    window['$REN'].update(disabled=disabled)
    window['$FEN'].update(disabled=disabled)


def disable_elements(disabled, window):
    global rodada

    for i in range(3):
        window[f'@{i}'].update(disabled=disabled)

    window['%TR'].update(disabled=False)

layout = [
    [
        sg.Text('IP: '), sg.InputText("localhost", size=(15, None), key='-IP-'),
        sg.Text('PORT: '), sg.InputText("8080", size=(10, None), key='-PORT-'),
        sg.Button('Conectar', key='conn')
    ],
    [
        sg.Button(image_source=verso, key='#0', disabled=True),
        sg.Button(image_source=verso, key='#1', disabled=True),
        sg.Button(image_source=verso, key='#2', disabled=True),
    ],
    [
        sg.Multiline(size=(40, 10), autoscroll=True, disabled=True, key='-MESA-'),
        sg.Column(pontos_p1), sg.Column(pontos_p2)
    ],
    [
        sg.Button(image_source=verso, key='@0', disabled=True),
        sg.Button(image_source=verso, key='@1', disabled=True),
        sg.Button(image_source=verso, key='@2', disabled=True),
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Button("Desistir", key='DES', disabled=True)
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Button("Envido", key='$EN', disabled=True),
        sg.Button("Real envido", key='$REN', disabled=True),
        sg.Button("Falta envido", key='$FEN', disabled=True),
        sg.Button("Flor", key='$FL', disabled=True),
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Button("Truco", key='%TR', disabled=True),
        sg.Button("Retruco", key='%RTR', disabled=True),
        sg.Button("Vale Quatro", key='%VQ', disabled=True)
    ]
]


def receber_mensagem(socket, window):
    global mostra_truco, mostra_envido

    while True:
        data = socket.recv(1024)

        if not data:
            continue

        try:
            data = pickle.loads(data)
            msg = data['ultima_mensagem']
            if len(msg) > 0:
                window['-MESA-'].print(msg)
        except:
            print(data)
        print(data)

        if data['id'] != id:
            rodada['cartas_oponente'].append(data['cartas_jogadas'])

        if data['truco'] > 0:
            mostra_truco = True
            rodada['valor_truco'] = data['truco']

        # if not data['pode_envido']:
        #     disable_envido(True, window)

        if len(rodada['cartas_oponente']) > 0:
            for carta in rodada['cartas_oponente']:
                if len(carta) > 0:
                    img_path = f"{path}{carta[1]}.png"
                    window[f'#{carta[0]}'].update(image_filename=img_path)


thread = None

window = sg.Window('SockeTruco', layout)

text_box = window['-MESA-']

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    while True:
        event, values = window.read(timeout=500)
        if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
            break

        resposta = {
            'jogador': id,
            'carta': None,
            'mensagem': "",
            'pediu_envido': 0,
            'pediu_truco': 0,
            'quero': None
        }

        if event == "conn":
            conectou = True
            HOST = values['-IP-']
            PORT = int(values['-PORT-'])

            s.connect((HOST, PORT))

            window['-IP-'].update(disabled=True)
            window['-PORT-'].update(disabled=True)
            window['conn'].update(disabled=True)

            mensagem_inicial_socket = pickle.loads(s.recv(1024))

            print(mensagem_inicial_socket)

            id = mensagem_inicial_socket[0]
            estado = mensagem_inicial_socket[1]

            print(estado)

            text_box.print(f"<Voce é o jogador {id}>")

            thread = threading.Thread(target=receber_mensagem, args=(s, window))
            thread.start()

            mao = estado['rodada'][f'cartas_p{id}']

            disable_elements(False, window)

            for i in range(3):
                img_path = f"{path}{mao[i].__str__()}.png"
                window[f'@{i}'].update(image_filename=img_path, disabled=False)

        if '@' in event:
            window[event].update(disabled=True)
            carta = int(event.replace('@', ''))
            num, naipe = mao[carta].num, mao[carta].naipe

            mensagem = f"<Jogador {id}> Jogou: {Carta.get_nome(num, naipe)}"
            text_box.print(mensagem)

            resposta['carta'] = carta
            resposta['mensagem'] = mensagem

        elif '$' in event:
            window[event].update(disabled=True)
            mensagem = f"<Jogador {id}> Pediu: envido"
            text_box.print(mensagem)

            resposta['pediu_envido'] = 1
            resposta['mensagem'] = mensagem

        elif '%' in event:
            window[event].update(disabled=True)
            mensagem = f"<Jogador {id}> Pediu: truco"
            text_box.print(mensagem)

            resposta['pediu_truco'] = 1
            resposta['mensagem'] = mensagem

        if mostra_truco:
            mostra_truco = False

            valor_truco = rodada['valor_truco']
            print(valor_truco)
            e, v = popups_truco[valor_truco-1].read(close=True)

            nome_pedido = ""

            if e != 'QUERO' and e != 'NÃO QUERO':
                resposta['pediu_truco'] = 1
                mensagem = f"<Jogador {id}> Pediu: {e}"
            else:
                if e == 'QUERO':
                    resposta['quero'] = True
                    mensagem = f"<Jogador {id}> QUERO!"
                else:
                    resposta['quero'] = False
                    mensagem = f"<Jogador {id}> Não quero..."

            text_box.print(mensagem)
            resposta['mensagem'] = mensagem

        if mostra_envido:
            mostra_envido = False
            e, v = pop_envido.read(close=True)


        if rodada['valor_truco'] > 0:
            valor = rodada['valor_truco']
            if valor == 1:
                window['%TR'].update(disabled=True)
            elif valor == 2:
                window['%RTR'].update(disabled=True)
            elif valor == 3:
                window['%VQ'].update(disabled=True)

        if conectou:
            s.send(pickle.dumps(resposta))

    window.close()

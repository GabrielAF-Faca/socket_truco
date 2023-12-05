import random

import PySimpleGUI as sg
from baralho import *
from cartas import *

while True:

    baralho = Baralho()

    baralho.embaralha()

    cartas = baralho.retorna6()
    mao = cartas[:3]
    mao_oponente = cartas[3:]

    jogadas_oponente = [i for i in range(len(mao_oponente))]

    keys = [f'@{carta.num};{carta.naipe}' for carta in mao]
    path = './cartas/'
    paths = {
        keys[0] : f'{path}{keys[0].replace(";", "").lstrip("@")}.png',
        keys[1] : f'{path}{keys[1].replace(";", "").lstrip("@")}.png',
        keys[2] : f'{path}{keys[2].replace(";", "").lstrip("@")}.png'
    }

    paths_oponente = [f'{path}{carta.num}{carta.naipe}.png' for carta in mao_oponente]

    src = './cartas/verso.png'
    mostrar_cartas = False

    sg.theme('Default1')  # Add a touch of color

    pontos_p1 = [[sg.Text("J1")], [sg.Text("0")]]
    pontos_p2 = [[sg.Text("J2")], [sg.Text("0")]]

    flor_disabled = True
    if cartas[0].naipe == cartas[1].naipe == cartas[2].naipe:
        flor_disabled = False

    layout = [
        [
            sg.Text('IP: '), sg.InputText(size=(15, None)),
            sg.Text('PORT: '), sg.InputText(size=(10, None)),
            sg.Button('Conectar')
         ],
        [
            sg.Button(image_source=src, key='#0', disabled=True),
            sg.Button(image_source=src, key='#1', disabled=True),
            sg.Button(image_source=src, key='#2', disabled=True),
        ],
        [
            sg.Multiline(size=(40, 10), autoscroll=True, disabled=True, key='-MESA-'),
            sg.Column(pontos_p1), sg.Column(pontos_p2)
        ],
        [
            sg.Button(image_source=src, key=f'@{cartas[0].num};{cartas[0].naipe}'),
            sg.Button(image_source=src, key=f'@{cartas[1].num};{cartas[1].naipe}'),
            sg.Button(image_source=src, key=f'@{cartas[2].num};{cartas[2].naipe}'),
        ],
        [sg.HorizontalSeparator()],
        [
            sg.Button("Desistir", key='DES')
        ],
        [sg.HorizontalSeparator()],
        [
            sg.Button("Envido", key='$EN'),
            sg.Button("Real envido", key='$REN'),
            sg.Button("Falta envido", key='$FEN'),
            sg.Button("Flor", disabled=flor_disabled, key='$FL'),
        ],
        [sg.HorizontalSeparator()],
        [
            sg.Button("Truco", key='%TR'),
            sg.Button("Retruco", key='%RTR'),
            sg.Button("Vale Quatro", key='%VQ')
        ]
    ]

    # Create the Window
    window = sg.Window('SockeTruco', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'DES':  # if user closes window or clicks cancel
            break

        text_box = window['-MESA-']

        if not mostrar_cartas:
            mostrar_cartas = True
            for key in window.key_dict:
                if '@' in str(key):
                    window[key].update(image_filename=paths[key])

        if '@' in event:
            window[event].update(disabled=True)
            num, naipe = event.replace('@', '').split(';')
            text_box.print(f"<Jogador 1> Jogou: {Carta.get_nome(num, naipe)}")

            carta = random.choice(jogadas_oponente)

            jogadas_oponente.remove(carta)
            window[f'#{carta}'].update(image_filename=paths_oponente[carta])
            text_box.print(f"<Jogador 2> Jogou: {mao_oponente[carta].get_own_nome()}")

        elif '$' in event:
            if event == '$FL':
                if not flor_disabled:
                    sg.Popup(window[event].get_text().lower(), title="Pontos", custom_text=("OK ", "CONTRAFLOR"))
                else:
                    sg.Popup(window[event].get_text().lower(), title="Pontos")
            else:
                sg.Popup(window[event].get_text().lower(), title="Pontos", custom_text=("QUERO ", "NÃO QUERO"))

        elif '%' in event:
            sg.Popup(window[event].get_text().lower(), title="Truco", custom_text=("QUERO ", "NÃO QUERO"))

    window.close()



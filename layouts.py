
import PySimpleGUI as sg

sg.theme('Default1')

global pop_truco
global pop_retruco
global pop_valequatro


truco_layout = [
    [sg.Text("TRUCO", justification='center')],
    [sg.HorizontalSeparator()],
    [sg.Button("QUERO"), sg.Button("NÃO QUERO"), sg.Button("ENVIDO"), sg.Button("RETRUCO")],
]

pop_truco = sg.Window('Truco', truco_layout, )

retruco_layout = [
    [sg.Text("RETRUCO", justification='center')],
    [sg.HorizontalSeparator()],
    [sg.Button("QUERO"), sg.Button("NÃO QUERO"), sg.Button("VALE QUATRO")],
]

pop_retruco = sg.Window('Retruco', retruco_layout)

valequatro_layout = [
    [sg.Text("VALE QUATRO", justification='center')],
    [sg.HorizontalSeparator()],
    [sg.Button("QUERO"), sg.Button("NÃO QUERO")],
]

pop_valequatro = sg.Window('Vale Quatro', valequatro_layout)

global pop_envido
global pop_realenvido
global pop_faltaenvido
global pop_flor
global pop_contraflor

envido_layout = [
    [sg.Text("ENVIDO", justification='center')],
    [sg.HorizontalSeparator()],
    [
        sg.Button("QUERO"),
        sg.Button("NÃO QUERO"),
        sg.Button("REAL ENVIDO"),
        sg.Button("FALTA ENVIDO"),
        sg.Button("FLOR", disabled=True)
    ],
]

pop_envido = sg.Window("Envido", envido_layout)

realenvido_layout = [
    [sg.Text("REAL ENVIDO", justification='center')],
    [sg.HorizontalSeparator()],
    [
        sg.Button("QUERO"),
        sg.Button("NÃO QUERO"),
        sg.Button("FALTA ENVIDO"),
        sg.Button("FLOR", disabled=True)
    ],
]

pop_realenvido = sg.Window("Real envido", realenvido_layout)

faltaenvido_layout = [
    [sg.Text("FALTA ENVIDO", justification='center')],
    [sg.HorizontalSeparator()],
    [
        sg.Button("QUERO"),
        sg.Button("NÃO QUERO"),
        sg.Button("FLOR", disabled=True)
    ],
]

pop_faltaenvido = sg.Window("Real envido", faltaenvido_layout)

flor_layout = [
    [sg.Text("FLOR", justification='center')],
    [sg.HorizontalSeparator()],
    [
        sg.Button("OK"),
        sg.Button("CONTRA FLOR", disabled=True)
    ],
]

pop_flor = sg.Window("Flor", flor_layout)

contraflor_layout = [
    [sg.Text("CONTRA FLOR", justification='center')],
    [sg.HorizontalSeparator()],
    [
        sg.Button("QUERO"),
        sg.Button("NÃO QUERO"),
    ],
]

pop_contraflor = sg.Window("Contra flor", contraflor_layout)
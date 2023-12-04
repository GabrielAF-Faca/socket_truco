import PySimpleGUI as sg
from baralho import *

baralho = Baralho()

baralho.embaralha()

cartas = baralho.retorna6()[:3]

srcs = [f'./cartas/{carta.num}{carta.naipe}.png' for carta in cartas]

sg.theme('Default1')  # Add a touch of color

pontos_p1 = [[sg.Text("J1")], [sg.Text("0")]]
pontos_p2 = [[sg.Text("J2")], [sg.Text("0")]]

layout = [
    [sg.Text('IP: '), sg.InputText(size=(15, None)), sg.Text('PORT: '), sg.InputText(size=(10, None)), sg.Button('Conectar')],
    [sg.Multiline(size=(40, 10), autoscroll=True, disabled=True), sg.Column(pontos_p1), sg.Column(pontos_p2)],
    [sg.Button(image_source=srcs[0]), sg.Button(image_source=srcs[1]), sg.Button(image_source=srcs[2]), sg.VerticalSeparator(), sg.Button("QUERO"), sg.Button("NÃO QUERO")],
    [sg.HorizontalSeparator()],
    [sg.Button("Desistir")],
    [sg.HorizontalSeparator()],
    [sg.Button("Envido"), sg.Button("Real envido"), sg.Button("Falta envido"), sg.Button("Flor"), sg.Button("Contraflor")],
    [sg.HorizontalSeparator()],
    [sg.Button("Truco"), sg.Button("Retruco"), sg.Button("Vale Quatro")]
]

# Create the Window
window = sg.Window('SockeTruco', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()
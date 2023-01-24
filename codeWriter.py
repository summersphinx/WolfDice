import PySimpleGUI as sg
from random import randint, choice

sg.theme(choice(sg.theme_list()))

layout = [
    [
        sg.Column([[sg.Listbox([], s=(10, 10), k='entries')]]),
        sg.Column(
                [
                    [sg.InputText('', do_not_clear=False, k='Input', s=(12, 1))],
                    [sg.Button('Enter', s=(10, 1))],
                    [sg.Button('Print', s=(10, 1))],
                    [sg.Button('Delete', s=(10, 1))]
                ])
    ]
]

wn = sg.Window('', layout)

event, values = wn.read()

wn.close()

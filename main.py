import PySimpleGUI as sg
import pandas as pd
import os
import sys

# values are:   with or without
CURRENT_SCREEN = 'with'
if sys.platform == 'win32':
    PATH = os.getenv('LOCALAPPDATA') + '/GEM Games/WolfDice/'
else:
    PATH = 'GEM Games/WolfDice/'

sg.theme('PythonPlus')
screen_left = [
    [sg.Frame('Output', [[sg.Multiline('', disabled=True, expand_y=True, expand_x=True)]], s=(310, 480))]
]

sg.theme('DarkGrey15')
screen_with = [
    [sg.Button('Switch to No Humans', expand_x=True, font='Arial 16 bold')],
    [sg.Text('Years: ', justification='right', expand_x=True, font='Arial 14 bold'), sg.Spin([i for i in range(1, 100)], initial_value=5, k='years_with', font='Arial 14 bold', s=(4, 1))],
    [sg.Text('Starting Pack: ', justification='right', expand_x=True, font='Arial 14 bold'), sg.Spin([i for i in range(1, 100)], initial_value=15, k='starting_with', font='Arial 14 bold', s=(4, 1))],
    [sg.Button('Reset Values', k='reset_with', expand_x=True, font='Arial 14 bold')],
    [sg.Button('Run Simulation', k='run_with', expand_x=True, font='Arial 14 bold')],
    [sg.Multiline('', disabled=True, k='data_with', expand_x=True, expand_y=True)]
]

sg.theme('Topanga')
screen_without = [
    [sg.Button('Switch to No Humans', expand_x=True, font='Arial 16 bold')],
    [sg.Text('Years: '), sg.Spin([i for i in range(1, 100)], initial_value=5, k='years_without'),
     sg.Text('Starting Pack: '), sg.Spin([i for i in range(1, 100)], initial_value=15, k='starting_without'),
     sg.Button('Reset Values', k='reset_without')],
    [sg.Button('Run Simulation', k='run_without')],
    [sg.Multiline('', disabled=True, k='data_without')]
]

WITH_ENABLED = False
if CURRENT_SCREEN.lower() == 'with':
    WITH_ENABLED = True

sg.theme('PythonPlus')
screen_right = [
    [sg.Frame('With Human Interaction', screen_with, visible=WITH_ENABLED, s=(310, 480)),
     sg.Frame('Without Human Interaction', screen_without, visible=not WITH_ENABLED, s=(310, 480))]
]

layout = [
    [
        sg.Column(screen_left),
        sg.Column(screen_right)
    ]
]

wn = sg.Window('Wolf Dice', layout)
event, values = wn.read()
wn.close()
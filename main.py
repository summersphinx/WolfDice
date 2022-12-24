import PySimpleGUI as sg
import pandas as pd
import os
import sys
import math
import numpy
import requests
from random import randint

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
    [sg.Text('Years: ', justification='right', expand_x=True, font='Arial 14 bold'),
     sg.Spin([i for i in range(1, 100)], initial_value=5, k='years_with', font='Arial 14 bold', s=(4, 1))],
    [sg.Text('Starting Pack: ', justification='right', expand_x=True, font='Arial 14 bold'),
     sg.Spin([i for i in range(1, 100)], initial_value=15, k='starting_with', font='Arial 14 bold', s=(4, 1))],
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


def run(years: int, starting: int, humans: bool) -> int:
    """

    :param years:  The amount of years to run the simulation for.
    :param starting: The amount of wolves starting in the pack.
    :param humans: Whether humans are involved in the packs' lives.
    :return: The amount of wolves remaining in the pack after a certain amount of years.
    """
    for t in range(years):
        print(t)
        number1 = randint(1, 6)  # int(requests.get("https://www.random.org/integers/?num=1&min=1&max=6&col=5&base=10&format=plain&rnd=new").text)
        number2 = randint(1, 6)  # int(requests.get("https://www.random.org/integers/?num=1&min=1&max=6&col=5&base=10&format=plain&rnd=new").text)

        if humans:
            if number1 == 2:
                if number2 in [2, 3]:
                    starting -= 2
                elif number2 == 1:
                    starting -= 1
                elif number2 == 6:
                    starting /= 2
            elif number1 == 3:
                if number2 in [3, 1, 2, 6]:
                    starting -= 2
                elif number2 == 5:
                    starting /= 2
            elif number1 == 4:
                if number2 in [4, 1, 5]:
                    starting -= 2
                elif number2 == 6:
                    starting -= 1
            elif number1 == 5:
                if number2 in [5, 4]:
                    starting -= 2
                elif number2 == 6:
                    starting -= 1
                elif number2 == 3:
                    starting /= 2
            elif number1 == 1:
                if number2 in [3, 4]:
                    starting -= 2
                elif number2 == 2:
                    starting -= 1
                elif number2 == 1:
                    starting /= 2
            elif number1 == 6:
                if number2 in [4, 5]:
                    starting -= 1
                elif number2 == 3:
                    starting -= 2
                elif number2 == 2:
                    starting /= 2
                elif number2 == 6:
                    starting += 1
        else:
            if number2 == number1 and number1 in [2, 3, 4, 5]:
                starting -= 2
            elif number2 == number1:
                if number1 == 1:
                    starting /= 2
                elif number1 == 6:
                    starting += 1
            elif number2 + number1 == 11:
                starting -= 1
            elif number1 in [2, 3] and [5, 6][[2, 3].index(number1)] == number2:
                starting /= 2
            elif number1 == 3 and number2 in [1, 5]:
                starting -= 2
            elif number2 in [1, 2] and number1 in [1, 2] and number1 + number2 == 3:
                starting -= 1
            elif number1 == 1 and number2 == 3:
                starting -= 2
            elif number1 == 2 and number2 == 6:
                starting /= 2
        starting = round(starting)
        starting += 5
    return starting


class Data:
    def Interpret(self, years, starting, humans):
        pass

    def Make(self, years, starting, humans):
        for i in range(10000):
            pass





wn = sg.Window('Wolf Dice', layout)
event, values = wn.read()
wn.close()

if __name__ == '__main__':
    print(run(5, 15, True))

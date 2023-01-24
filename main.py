import os
import statistics as stats
import sys
from random import randint

import PySimpleGUI as sg

# values are:   with or without
CURRENT_SCREEN = 'with'
if sys.platform == 'win32':
    PATH = os.getenv('LOCALAPPDATA') + '/GEM Games/WolfDice/'
else:
    PATH = 'GEM Games/WolfDice/'

os.makedirs(PATH, exist_ok=True)

sg.theme('PythonPlus')
screen_left = [
    [sg.Frame('Output', [[sg.Multiline('', disabled=True, expand_y=True, expand_x=True, k='output')]], s=(310, 480))]
]

sg.theme('DarkGrey15')
screen_with = [
    [sg.Button('Switch to No Humans', expand_x=True, font='Arial 16 bold', k='swo')],
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
    [sg.Button('Switch to Humans', expand_x=True, font='Arial 16 bold', k='sw')],
    [sg.Text('Years: ', justification='right', expand_x=True, font='Arial 14 bold'),
     sg.Spin([i for i in range(1, 100)], initial_value=5, k='years_without', font='Arial 14 bold', s=(4, 1))],
    [sg.Text('Starting Pack: ', justification='right', expand_x=True, font='Arial 14 bold'),
     sg.Spin([i for i in range(1, 100)], initial_value=15, k='starting_without', font='Arial 14 bold', s=(4, 1))],
    [sg.Button('Reset Values', k='reset_without', expand_x=True, font='Arial 14 bold')],
    [sg.Button('Run Simulation', k='run_without', expand_x=True, font='Arial 14 bold')],
    [sg.Multiline('', disabled=True, k='data_without', expand_x=True, expand_y=True)]
]

WITH_ENABLED = False
if CURRENT_SCREEN.lower() == 'with':
    WITH_ENABLED = True

sg.theme('PythonPlus')
screen_right = [
    [sg.Frame('With Human Interaction', screen_with, visible=WITH_ENABLED, s=(310, 480), k='w'),
     sg.Frame('Without Human Interaction', screen_without, visible=not WITH_ENABLED, s=(310, 480), k='wo')]
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

    # sg.cprint('Running Simulation . . .')
    for t in range(years):
        number1 = randint(1,
                          6)  # int(requests.get("https://www.random.org/integers/?num=1&min=1&max=6&col=5&base=10&format=plain&rnd=new").text)
        number2 = randint(1,
                          6)  # int(requests.get("https://www.random.org/integers/?num=1&min=1&max=6&col=5&base=10&format=plain&rnd=new").text)

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


def Make(years, starting, humans, path):
    a = open('{}{} {} {} data.wddata'.format(path, years, starting, humans), 'a')
    bar = sg.Window('Progress {} {} {} data'.format(years, starting, humans), [[sg.ProgressBar(10000, k='bar')]],
                    finalize=True)
    for i in range(10000):
        a.write(str(run(years, starting, humans)) + '\n')
        bar['bar'].update(current_count=i)
    a.close()
    bar.close()


def Read(years, starting, humans, path):
    try:
        with open('{}{} {} {} data.wddata'.format(path, years, starting, humans), 'r') as a:
            raw_data = a.readlines()
        data = []
        for each in raw_data:
            data.append(int(each[:-1]))
        return data

    except FileNotFoundError:
        Make(years, starting, humans, PATH)
        Read(years, starting, humans, PATH)


def Interpret(raw):
    sg.cprint('Getting Stats . . .')
    avg = "Average: " + str(stats.mean(raw)) + '\n'
    mode = "Mode: " + str(stats.mode(raw)) + '\n'
    med = "Median: " + str(stats.median(raw)) + '\n\n ------- \n\n'
    fifty = "50th Percentile: " + str(stats.median_grouped(raw)) + '\n'
    variance = "Variance: " + str(stats.variance(raw)) + '\n\n ------- \n\n'
    length = "# of Simulations: " + str(len(raw)) + '\n'

    return avg + mode + med + fifty + variance + length


class WolfDice:
    def __init__(self, years, starting, humans):
        pass


if __name__ == '__main__':
    wn = sg.Window('Wolf Survival is Just a Roll Away ...', layout, finalize=True)
    sg.cprint_set_output_destination(wn, 'output')
    while True:
        event, values = wn.read()

        if event == sg.WIN_CLOSED:
            break

        if event in ('sw', 'swo'):
            sg.cprint('Switching modes . . .')
            WITH_ENABLED = not WITH_ENABLED
            wn['w'].Update(visible=WITH_ENABLED)
            wn['wo'].Update(visible=not WITH_ENABLED)
        if event in ('run_without', 'run_with'):
            raw = None
            if WITH_ENABLED:
                while raw is None:
                    raw = Read(values['years_with'], values['starting_with'], WITH_ENABLED, PATH)
            else:
                while raw is None:
                    raw = Read(values['years_without'], values['starting_without'], WITH_ENABLED, PATH)

            data = Interpret(raw)
            wn['data_with'].Update(data)
            wn['data_without'].Update(data)

    wn.close()

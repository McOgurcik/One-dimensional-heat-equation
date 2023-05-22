import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
import PySimpleGUI as sg
import math as m
import matplotlib as mt
import time as ti
from matplotlib import animation
# mt.use('agg')
length = 1
d = 1
time = 4
dx = 0.02
temperature_start = 10
temperature = 0
class Canvas(FigureCanvasTkAgg):
    """
    Create a canvas for matplotlib pyplot under tkinter/PySimpleGUI canvas
    """
    def __init__(self, figure=None, master=None):
        super().__init__(figure=figure, master=master)
        self.canvas = self.get_tk_widget()
        self.canvas.pack(side='top', fill='both', expand=1)
def cm_to_inch(value):
    return value/2.54
def renew(n,p,t,t_next):
    for j in range(1, n - 1):
        # t_next[j] = p * t[j + 1] + (1 - 2 * p) * t[j] + p * t[j - 1];
        t_next[j] = p * t[j + 1] + (1 - 2 * p) * t[j] + p * t[j - 1]
    # print(t_next)
    for j in range(1, n - 1):
        t[j] = t_next[j]
    return t, t_next

def plot_figure(length,d,time,dx,temperature_start,temperature):
    dt = (dx * dx) / (2 * d)
    n = int((length / dx)) + 1
    t = [0 for i in range(n)]
    t_next = [0 for i in range(n)]
    x = [i*dx for i in range(n)]
    t[0] = temperature_start
    t_next[0] = temperature_start
    t_next[n - 1] = temperature
    p = (dt * d) / (dx * dx)
    for i in range(1, n):
        t[i] = temperature
    line, = ax.plot(x, t, color='g')  # Запомнить ссылку на линию графика
    plt.ion()

    k = 0.0
    while k <= time:
        ax.relim(visible_only=True)  # Пересчет границ осей
        # ax.autoscale_view(True)  # Автоматическое масштабирование осей
        ax.autoscale()
        canvas.draw()
        plt.pause(0.001)
        t, t_next = renew(n,p,t,t_next)
        line.set_data(x, t)  # Обновление данных графика
        event, values = window.read(timeout=0)
        if event in (sg.WIN_CLOSED, 'Exit'):
            ax.cla()
            plt.ioff()
            break
    plt.ioff()
    # plt.show()
sg.theme('DefaultNoMoreNagging')

layout = [
    [sg.Canvas(size=(640, 480), key='Canvas')],
    [sg.Text(text="length"),sg.Spin([i/10 for i in range(1,1000)], initial_value=length,enable_events=True, k='-L-'),
    sg.Text(text="d"),sg.Spin([i/10 for i in range(1,1000)], initial_value=d,enable_events=True, k='-D-'),
    sg.Text(text="time"),sg.Spin([i for i in range(1,70)], initial_value=time,enable_events=True, k='-T-'),
    sg.Text(text="dx"),sg.Spin([i/100 for i in range(1,1000)], initial_value=dx,enable_events=True, k='-DX-'),
    sg.Text(text="temperature_start"),sg.Spin([i/10 for i in range(0,1000)], initial_value=temperature_start,enable_events=True, k='-TS-'),
    sg.Text(text="temperature"),sg.Spin([i/10 for i in range(0,1000)], initial_value=temperature,enable_events=True, k='-TR-')],
    [sg.Button('Рассчитать')],
    # [sg.Text(text="α"),
    #  sg.Slider(range=(0, 90), default_value=a, size=(10, 20), expand_x=True, enable_events=True, orientation='h', key='Slider')],
    # [sg.Text(text="v0"),
     # sg.Slider(range=(0, 100), default_value=v0, size=(10, 20), expand_x=True, enable_events=True, orientation='h', key='v')],
     # [sg.Checkbox('Препятствие', default=False,enable_events=True, k='-P-')],
    [sg.Push(), sg.Button('Exit'), sg.Push()],
]
window = sg.Window('Температуропроводность', layout, finalize=True, resizable=True)

fig = Figure(figsize=(cm_to_inch(15), cm_to_inch(10)))
ax = fig.add_subplot()

canvas = Canvas(fig, window['Canvas'].Widget)
# fig = Figure(figsize=(cm_to_inch(15), cm_to_inch(10)))
# plt.ion()
# ax = fig.add_subplot()
# n = int((length / dx)) + 1
# x = [i*dx for i in range(n)]
# t = [0 for i in range(n)]
# line, = ax.plot(x, t, color='g')  # Запомните ссылку на линию графика
# canvas = Canvas(fig, window['Canvas'].Widget)


plot_figure(length,d,time,dx,temperature_start,temperature)

while True:

    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Рассчитать':
        plot_figure(length,d,time,dx,temperature_start,temperature)
    elif event == '-L-':
        # print(values)
        length = values[event]
    elif event == '-D-':
        # print(values)
        d = values[event]
    elif event == '-T-':
        # print(values)
        time = values[event]
    elif event == '-DX-':
        # print(values)
        dx = values[event]
    elif event == '-TS-':
        # print(values)
        temperature_start = values[event]
    elif event == '-TR-':
        # print(values)
        temperature = values[event]
# 8. Close window to exit

window.close()

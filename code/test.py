import numpy as np

# x = np.arange(9)

# print(x)

# # x[:-1] = x[1:]
# # x[-1] = 9

# x = np.roll(x, -1)
# x[-1] = 9

# print(x)

# x = np.array([[],[]])
# print(x.shape)

# import time

# import matplotlib.pyplot as plt
# import numpy

# def gaussian(x, delay, sigma):
#     '''
#     Функция, график которой будет отображаться процессе анимации
#     '''
#     return numpy.exp(-((x - delay) / sigma) ** 2)

# if __name__ == '__main__':
#     # Параметры отображаемой функции
#     maxSize = 200
#     sigma = 10.0

#     # Диапазон точек для расчета графика функции
#     x = numpy.arange(maxSize)

#     # Значения графика функции
#     y = numpy.zeros(maxSize)

#     # !!! Включить интерактивный режим для анимации
#     plt.ion()

#     # У функции gaussian будет меняться параметр delay (задержка)
#     for delay in numpy.arange(-50.0, 200.0, 1.0):
#         y = gaussian(x, delay, sigma)

#         # !!! Очистить текущую фигуру
#         plt.clf()

#         # Отобразить график
#         plt.plot(x, y)

#         # Установка отображаемых интервалов по осям
#         plt.xlim(0, maxSize)
#         plt.ylim(-1.1, 1.1)

#         # !!! Следующие два вызова требуются для обновления графика
#         plt.draw()
#         plt.gcf().canvas.flush_events()

#         # Задержка перед следующим обновлением
#         time.sleep(0.005)

#     # Отключить интерактивный режим по завершению анимации
#     plt.ioff()

#     # Нужно, чтобы график не закрывался после завершения анимации
#     plt.show()

# import time

# import matplotlib.pyplot as plt
# import numpy

# def gaussian(x, delay, sigma):
#     '''
#     Функция, график которой будет отображаться процессе анимации
#     '''
#     return numpy.exp(-((x - delay) / sigma) ** 2)

# if __name__ == '__main__':
#     # Параметры отображаемой функции
#     maxSize = 200
#     sigma = 10.0

#     # Диапазон точек для расчета графика функции
#     x = numpy.arange(maxSize)

#     # Значения графика функции
#     y = numpy.zeros(maxSize)

#     # !!! Включить интерактивный режим для анимации
#     plt.ion()

#     # Создание окна и осей для графика
#     fig, ax = plt.subplots()

#     # Установка отображаемых интервалов по осям
#     ax.set_xlim(0, maxSize)
#     ax.set_ylim(-1.1, 1.1)

#     # Отобразить график фукнции в начальный момент времени
#     line, = ax.plot(x, y)

#     # У функции gaussian будет меняться параметр delay (задержка)
#     for delay in numpy.arange(-50.0, 200.0, 1.0):
#         y = gaussian(x, delay, sigma)

#         # Обновить данные на графике
#         line.set_ydata(y)

#         # Отобразить новые данный
#         fig.canvas.draw()
#         fig.canvas.flush_events()

#         # Задержка перед следующим обновлением
#         time.sleep(0.001)

#     # Отключить интерактивный режим по завершению анимации
#     plt.ioff()
#     plt.show()

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy


def gaussian(x, delay, sigma):
    '''
    Функция, график которой будет отображаться процессе анимации.
    '''
    return numpy.exp(-((x - delay) / sigma)**2)


# Функция, вызываемая для каждого кадра
def main_func(frame, line, x, sigma):
    '''
    frame - параметр, который изменяется от кадра к кадру.
    line - кривая, для которой изменяются данные.
    x - список точек по оси X, для которых рассчитывается функция Гаусса.
    sigma - отвечает за ширину функции Гаусса.
    '''
    y = gaussian(x, frame, sigma)
    line.set_ydata(y)
    return [line]


if __name__ == '__main__':
    # Параметры отображаемой функции
    maxSize = 200
    sigma = 10.0

    # Диапазон точек для расчета графика функции
    x = numpy.arange(maxSize)

    # Значения графика функции
    y = numpy.zeros(maxSize)

    # Создание окна для графика
    fig, ax = plt.subplots()

    # Установка отображаемых интервалов по осям
    ax.set_xlim(0, maxSize)
    ax.set_ylim(-1.1, 1.1)

    # Создание линии, которую будем анимировать
    line, = ax.plot(x, y)

    # !!! Параметр, который будет меняться от кадра к кадру
    frames = numpy.arange(-50.0, 200.0, 1.0)

    # !!! Задержка между кадрами в мс
    interval = 30

    # !!! Использовать ли буферизацию для устранения мерцания
    blit = True

    # !!! Будет ли анимация циклической
    repeat = False

    # !!! Создание анимации
    animation = FuncAnimation(fig,
                              func=main_func,
                              frames=frames,
                              fargs=(line, x, sigma),
                              interval=interval,
                              blit=blit,
                              repeat=repeat)
    plt.show()
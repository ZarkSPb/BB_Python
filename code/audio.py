import pyaudio as pa
import numpy as np
# import matplotlib.pyplot as plt

np.set_printoptions(precision=5, linewidth=2000, threshold=2000, suppress=True)

PI2 = 2 * np.pi
# длительность звука
duration_tone = 1 / 1.0
# частота дискретизации выходного сигнала
SAMPLE_RATE = 24000
# 16-ти битный звук (2 ** 16 -- максимальное значение для int16)
S_16BIT = 2**15 - 1
# озвучиваемая частота
freq = 311.13

i = 0

t = np.arange((i) * duration_tone, (i + 1) * duration_tone, 1 / SAMPLE_RATE)
# tone = np.array(np.sin(PI2 * freq * t) * S_16BIT, dtype=np.int16)
tone = np.array(np.sin(PI2 * freq * t) * S_16BIT, dtype=np.int16)

print(tone[0])
print(tone[-1])

# fig, ax = plt.subplots()
# ax.plot(tone[:451])
# plt.show()

# инициализируем
p = pa.PyAudio()
# создаём поток для вывода
stream = p.open(format=p.get_format_from_width(width=2),
                channels=1,
                rate=SAMPLE_RATE,
                output=True)

stream.write(tone)
stream.write(tone)
stream.write(tone)
stream.write(tone)
stream.write(tone)
stream.write(tone)

# останавливаем устройство
stream.stop_stream()
# завершаем работу PyAudio
stream.close()
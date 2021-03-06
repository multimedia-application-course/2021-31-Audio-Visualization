# coding = utf-8
import numpy as np
import pyaudio
from pydub import AudioSegment, effects
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

file_path = input("请输入要播放的音乐文件名/路径(wav格式)：")

# 新建PyAudio对象
p = pyaudio.PyAudio()
sound = AudioSegment.from_file(file=file_path)
left = sound.split_to_mono()[0]
fs = left.frame_rate
size = len(left.get_array_of_samples())
channels = left.channels
stream = p.open(
    format=p.get_format_from_width(left.sample_width, ),
    channels=channels,
    rate=fs,
    # input=True,
    output=True,
)
stream.start_stream()

fig = plt.figure()
ax1, ax2 = fig.subplots(2, 1)
# ax1 = fig.subplots()
ax1.set_ylim(0, 2)
ax2.set_ylim(-1.5, 1.5)
# ax1.set_axis_off()
# ax2.set_axis_off()
ax1.set_xticks([])
ax1.set_yticks([])
ax2.set_xticks([])
ax2.set_yticks([])
window = int(0.02 * fs)  # 20ms帧速率

g_windows = window // 8


f = np.linspace(20, 20 * 1000, g_windows)
t = np.linspace(0, 20, window)
lf1, = ax1.plot(f, np.zeros(g_windows), lw=1)
lf1.set_antialiased(True)
lf1.set_fillstyle('left')
lf1.set_drawstyle('steps-pre')
lf2, = ax2.plot(t, np.zeros(window), lw=1)

color_grade = ['black','blue','yellow','red']
def update(frames):
    if stream.is_active():
        slice = left.get_sample_slice(frames, frames + window)
        data = slice.raw_data
        stream.write(data)
        y = np.array(slice.get_array_of_samples()) / 30000  # 归一化
        yft = np.abs(np.fft.fft(y)) / (g_windows) # 快速傅里叶变换
        # print('max',max(yft[:g_windows]),'min',min(yft[:g_windows]))
        # print(max(yft[:g_windows]) - min(yft[:g_windows]))
        # max = max(yft[:g_windows])
        # min = min(yft[:g_windows])
        grade = int(max(yft[:g_windows]) - min(yft[:g_windows]))
        if 0 <= grade < len(color_grade):
            lf1.set_color(color_grade[grade])
        lf1.set_ydata(yft[:g_windows])
        lf2.set_ydata(y)
    # return lf1,
    return lf1, lf2,


ani = FuncAnimation(fig, update, frames=range(0, size, window), interval=0, blit=True)
plt.show()

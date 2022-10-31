import tkinter as tk
import tkinter.ttk as ttk
import pygame
from random import choice, randint
from string import ascii_uppercase, digits
from time import sleep

# Вариант №6 — использование весовых коэффициентов и генерация ключа с учётом попадания среднего значения в диапазон

# Словарь весовых коэффициентов, распределённых случайно от 1 до количества букв и цифр
weights = {le: randint(1, 36) for le in ascii_uppercase + digits}
sizes_of_blocks = [5, 4, 4]  # Размеры блоков ключа
# Интервал для средних значений блоков ключа (average_start — начало интервала, average_end — конец интервала)
interval_size = 5
average_start = randint(min(weights.values()) * max(sizes_of_blocks), max(weights.values()) - interval_size)
average_end = average_start + interval_size


def generate_block(length: int) -> str:
    # Генерирует один блок длины length для ключа
    # avrg = sum / amount, тогда sum = avrg * amount
    sum_start, sum_end = average_start * length, average_end * length

    # Случайным образом выбираем length букв из словаря weights
    # и проверяем, что их сумма укладывается в sum_start и sum_end
    block = [choice(list(weights.items())) for _ in range(length)]
    while sum(map(lambda x: x[1], block)) not in range(sum_start, sum_end + 1):
        block = [choice(list(weights.items())) for _ in range(length)]

    return ''.join(map(lambda x: x[0], block))  # Формируем и возвращаем блок ключа


def generate_key():
    # Генерирует ключ из блоков, размеры которых указаны в sizes_of_blocks
    blocks, progress_bar['value'] = [], 0
    for length_block in sizes_of_blocks:
        for _ in range(length_block):  # Допзадание: анимация с использованием прогрессбара
            progress_bar['value'] += 10
            wndw.update_idletasks()
            sleep(0.1)
        blocks.append(generate_block(length_block))
    lbl_key_field.configure(text='-'.join(blocks))  # Формируем ключ и отображаем его в лейбле


print(weights)
print(f'{average_start} <= avrg <= {average_end}')

wndw = tk.Tk()
wndw.title('Генератор ключа')
wndw.geometry('700x250')

pygame.init()   # Допзадание: использование музыки через pygame
pygame.mixer.init()
pygame.mixer.music.load("green hill soundtrack.mp3")

bg = tk.PhotoImage(file='bg.png')
lbl_bg = tk.Label(wndw, image=bg)
lbl_bg.place(x=0, y=0)

frame = tk.Frame(wndw)
frame.place(relx=0.5, rely=0.5, anchor='center')

lbl_key = tk.Label(frame, text='Ключ', font=('VK Sans Display', 12))
lbl_key.grid(column=1, row=0, padx=10, pady=10)


lbl_key_field = tk.Label(frame, text='', font=('VK Sans Display', 20))
lbl_key_field.grid(column=1, row=1, padx=10, pady=10)


btn_generate = tk.Button(frame, text='Сгенерировать', font=('VK Sans Display', 12), command=generate_key)
btn_generate.grid(column=0, row=2, padx=20, pady=20)

btn_exit = tk.Button(frame, text='Выйти', font=('VK Sans Display', 12), command=wndw.destroy)
btn_exit.grid(column=2, row=2, padx=63, pady=20)

progress_bar = ttk.Progressbar(frame, orient='horizontal', maximum=sum(sizes_of_blocks) * 10, mode='determinate')
progress_bar.grid(column=1, row=3, padx=10, pady=10)

pygame.mixer.music.play(-1)
wndw.mainloop()

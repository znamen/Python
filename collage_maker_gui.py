from tkinter import Tk, filedialog, Label, StringVar, Frame, Canvas
from PIL import Image, ImageTk
import os
import sys
import time

def create_collage(images, output_name, collage_size=(1920, 1080), margin_horizontal=40, margin_vertical=80, spacing=20, template=2):
    left_width = collage_size[0] // 2
    right_width = collage_size[0] - left_width
    right_height = collage_size[1]

    collage = Image.new('RGB', collage_size, (255, 255, 255))

    # Левое изображение
    left_image = Image.open(images[0])
    left_image = resize_and_crop(left_image, left_width, collage_size[1])
    collage.paste(left_image, (0, 0))

    if template == 1:
        # Настройка правой части для шаблона 1 и 3 (4 изображения по центру)
        rows = 2
        cols = 2
        total_margin_vertical = 2 * margin_vertical + spacing
        total_margin_horizontal = 2 * margin_horizontal + spacing
        thumbnail_height = (right_height - total_margin_vertical) // rows
        thumbnail_width = (right_width - total_margin_horizontal) // cols
        right_images = images[1:5]

        # Вычисляем общие отступы сверху и снизу для центровки
        total_images_height = rows * thumbnail_height + (rows - 1) * spacing
        total_margin_vertical = (right_height - total_images_height) // 2

        for i, image_path in enumerate(right_images):
            img = Image.open(image_path)
            img = resize_and_crop(img, thumbnail_width, thumbnail_height)

            # Позиции для изображения (выравнивание по центру)
            x = left_width + margin_horizontal + (i % cols) * (thumbnail_width + spacing)
            y = total_margin_vertical + (i // cols) * (thumbnail_height + spacing)
            collage.paste(img, (x, y))

    elif template == 2:
        # Настройка правой части для шаблона 2
        rows = 2
        cols = 1
        total_margin = 2 * margin_vertical + spacing
        thumbnail_height = (right_height - total_margin) // rows
        thumbnail_width = right_width - 2 * margin_horizontal
        right_images = images[1:3]

        for i, image_path in enumerate(right_images):
            img = Image.open(image_path)
            img = resize_and_crop(img, thumbnail_width, thumbnail_height)
            
            # Позиции для изображения
            x = left_width + margin_horizontal
            y = margin_vertical + i * (thumbnail_height + spacing)
            collage.paste(img, (x, y))

    elif template == 3:
            # Настройка правой части для шаблона 3 с отступами
            margin = 40  # Отступы от всех углов

            # Левое изображение
            left_width = (collage_size[0] // 2) - margin  # Ширина левого изображения с учетом отступа
            left_height = collage_size[1] - 2 * margin  # Высота с учетом отступов сверху и снизу
            left_image = Image.open(images[0])  
            left_image = resize_and_crop(left_image, left_width, left_height)  # Изменение размера
            collage.paste(left_image, (margin, margin))  # Позиционирование с отступом

            # Правое изображение
            right_width = (collage_size[0] // 2) - margin  # Ширина правого изображения с учетом отступа
            right_height = collage_size[1] - 2 * margin  # Высота правого изображения с учетом отступа
            right_image = Image.open(images[1])  
            right_image = resize_and_crop(right_image, right_width, right_height)  # Изменение размера
            collage.paste(right_image, (left_width + 2 * margin, margin))  # Позиционирование с отступом



    collage.save(output_name)
    print(f"Коллаж сохранён как {output_name}")


def resize_and_crop(image, width, height):
    img_ratio = image.width / image.height
    target_ratio = width / height

    if img_ratio > target_ratio:
        new_width = int(height * img_ratio)
        new_height = height
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        left = (new_width - width) // 2
        image = image.crop((left, 0, left + width, height))
    else:
        new_width = width
        new_height = int(width / img_ratio)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        top = (new_height - height) // 2
        image = image.crop((0, top, width, top + height))

    return image


def select_files():
    files = filedialog.askopenfilenames(title="Выберите изображения", filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
    if files:
        selected_files_label.config(text=f"Выбрано {len(files)} файлов", fg="white")
        global selected_images
        selected_images = files


def create_and_save_collage():
    if not selected_images:
        selected_files_label.config(text="Сначала выберите файлы!", fg="white")
        return
    
    # Генерация уникального имени на основе времени
    output_file = f"collage_{int(time.time() * 1000)}.jpg"  # Уникальное имя на основе времени (в миллисекундах)
    
    template = int(template_var.get())

    create_collage(selected_images, output_file, template=int(template))
    selected_files_label.config(text=f"Коллаж сохранён: {output_file}", fg="white")
    root.after(2000, lambda: selected_files_label.config(text=""))


def set_template(template_num):
    template_var.set(template_num)
    canvas_1.config(bg="#212121", highlightthickness=0)
    canvas_2.config(bg="#212121", highlightthickness=0)
    canvas_3.config(bg="#212121", highlightthickness=0)
    if template_num == 1:
        canvas_1.config(bg="#676767", highlightthickness=2, highlightbackground="white")
    elif template_num == 2:
        canvas_2.config(bg="#676767", highlightthickness=2, highlightbackground="white")
    elif template_num == 3:
        canvas_3.config(bg="#676767", highlightthickness=2, highlightbackground="white")


def create_oval_button(parent, text, command, width=150, height=50, bg="#212121", fg="white", radius=20):
    canvas = Canvas(parent, width=width, height=height, bg="#212121", highlightthickness=0)

    # Рисуем прямоугольник с закругленными углами
    canvas.create_oval(0, 0, radius * 2, radius * 2, fill=bg, outline="")
    canvas.create_oval(width - radius * 2, 0, width, radius * 2, fill=bg, outline="")
    canvas.create_oval(0, height - radius * 2, radius * 2, height, fill=bg, outline="")
    canvas.create_oval(width - radius * 2, height - radius * 2, width, height, fill=bg, outline="")
    
    # Рисуем оставшиеся части прямоугольника
    canvas.create_rectangle(radius, 0, width - radius, height, fill=bg, outline="")
    canvas.create_rectangle(0, radius, width, height - radius, fill=bg, outline="")

    text_id = canvas.create_text(width // 2, height // 2, text=text, fill=fg, font=("Arial", 12, "bold"))
    canvas.bind("<Button-1>", lambda event: command())

    # Добавляем обработку событий для наведения и ухода мыши
    def on_enter(event):
        canvas.itemconfig("all", fill="#313131")  # Меняем цвет на более светлый серый
        canvas.itemconfig(text_id, fill="#FFFFFF")  # Оставляем белый цвет текста

    def on_leave(event):
        canvas.itemconfig("all", fill=bg)  # Возвращаем исходный цвет
        canvas.itemconfig(text_id, fill=fg)  # Возвращаем исходный цвет текста

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)

    return canvas

# Перетаскивание окна
def on_drag_start(event):
    global x_offset, y_offset
    x_offset = event.x
    y_offset = event.y

def on_drag_motion(event):
    delta_x = event.x - x_offset
    delta_y = event.y - y_offset
    root.geometry(f"+{root.winfo_x() + delta_x}+{root.winfo_y() + delta_y}")

# Закрытие окна
def close_window():
    root.quit()

# Инициализация окна
root = Tk()
root.title("Collage Maker")
root.geometry("500x500+100+100")
root.config(bg="#212121")
root.overrideredirect(True)  # Скрыть заголовок окна

root.bind("<Button-1>", on_drag_start)  # Начало перетаскивания
root.bind("<B1-Motion>", on_drag_motion)  # Перетаскивание

selected_images = []

# Загружаем картинку
logo = Image.open("logo.jpg")
logo = logo.resize((120, 35))  # При необходимости измените размер
logo_img = ImageTk.PhotoImage(logo)

# Убираем текст, заменяем на картинку
Label(root, image=logo_img, bg="#212121").pack(pady=20)

template_var = StringVar(root)
template_var.set("2")

template_frame = Frame(root, bg="#212121")
template_frame.pack(pady=20)

# Используем sys._MEIPASS для правильного пути к изображениям после упаковки
def get_image_path(image_name):
    if getattr(sys, 'frozen', False):
        # Если запущено как EXE, используем _MEIPASS
        app_path = sys._MEIPASS
    else:
        # Если в процессе разработки, используем текущую директорию
        app_path = os.path.dirname(__file__)
    return os.path.join(app_path, image_name)

template_1_img = Image.open(get_image_path("template1.jpg")).resize((100, 100))
template_1_img = ImageTk.PhotoImage(template_1_img)

template_2_img = Image.open(get_image_path("template2.jpg")).resize((100, 100))
template_2_img = ImageTk.PhotoImage(template_2_img)

template_3_img = Image.open(get_image_path("template3.jpg")).resize((100, 100))
template_3_img = ImageTk.PhotoImage(template_3_img)

canvas_1 = Canvas(template_frame, width=100, height=100, bg="#212121", highlightthickness=0)
canvas_1.grid(row=0, column=0, padx=10)
canvas_1.create_image(0, 0, anchor="nw", image=template_1_img)
canvas_1.bind("<Button-1>", lambda event, template=1: set_template(template))

canvas_2 = Canvas(template_frame, width=100, height=100, bg="#212121", highlightthickness=0)
canvas_2.grid(row=0, column=1, padx=10)
canvas_2.create_image(0, 0, anchor="nw", image=template_2_img)
canvas_2.bind("<Button-1>", lambda event, template=2: set_template(template))

canvas_3 = Canvas(template_frame, width=100, height=100, bg="#212121", highlightthickness=0)
canvas_3.grid(row=0, column=2, padx=10)
canvas_3.create_image(0, 0, anchor="nw", image=template_3_img)  # Используем правильное изображение
canvas_3.bind("<Button-1>", lambda event, template=3: set_template(template))

set_template(1)

button_frame = Frame(root, bg="#212121", padx=10, pady=10)
button_frame.pack(pady=20)

create_oval_button(button_frame, "Выбрать файлы", select_files).pack(pady=10)
create_oval_button(button_frame, "Создать коллаж", create_and_save_collage).pack(pady=10)

log_frame = Frame(root, bg="#676767", pady=5)
log_frame.pack(side="bottom", fill="x")

selected_files_label = Label(log_frame, text="Файлы не выбраны", fg="white", bg="#676767")
selected_files_label.grid(row=0, column=0, padx=10, sticky="w")

# Функция для позиционирования кнопки закрытия
def position_close_button(event=None):
    close_button.place(x=root.winfo_width() - 40, y=10)

# Кнопка закрытия
close_button = Canvas(root, width=30, height=30, bg="#212121", highlightthickness=0)
close_button.create_text(15, 15, text="х", fill="white", font=("Arial", 12, "bold"))
close_button.place(x=root.winfo_width() - 40, y=10)  # Изначальное положение
close_button.bind("<Button-1>", lambda event: close_window())

# Привязка функции для изменения позиции кнопки при изменении размера окна
root.bind("<Configure>", position_close_button)

root.mainloop()

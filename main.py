import cv2
import pytesseract
from PIL import Image as PILImage
import pyautogui
import os
import time

time.sleep(1)

def take_screenshot(output_path):
    screenshot = pyautogui.screenshot()
    screenshot.save(output_path)


screenshot_path = 'screenshot.png'
take_screenshot(screenshot_path)

# Путь к папке с проектом
project_folder = os.path.dirname(os.path.abspath(__file__))

# Путь к папке для неудачных скриншотов
failed_screens_folder = os.path.join(project_folder, 'failed_screens')

# Функция для создания папки, если её не существует
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Создаем папку для неудачных скриншотов, если её нет
create_folder_if_not_exists(failed_screens_folder)

# Функция для создания папки с именем переменной text_eng
def create_folder_for_text(text):
    folder_path = os.path.join(failed_screens_folder, text)
    create_folder_if_not_exists(folder_path)
    return folder_path

# Функция для сохранения скриншота и текстового файла в папку
def save_failed_screenshot(text, screenshot_path, text_eng):
    folder_path = create_folder_for_text(text_eng)
    # Сохраняем скриншот рабочего стола
    desktop_screenshot_path = os.path.join(folder_path, 'desktop_screenshot.png')
    take_screenshot(desktop_screenshot_path)
    # Сохраняем текстовый файл с английским и русским текстом
    text_file_path = os.path.join(folder_path, 'texts.txt')
    with open(text_file_path, 'w') as f:
        f.write(f"English: {text}\n")
        f.write("Russian:\n")
        for russian_text in russian_texts:
            f.write(f"{russian_text}\n")

# Функция для создания скриншота экрана и сохранения его в файл
def take_screenshot(output_path):
    screenshot = pyautogui.screenshot()
    screenshot.save(output_path)

# Функция для обрезки изображения
def crop_image(input_path, output_path, width, height, x_offset, y_offset):
    img = PILImage.open(input_path)
    # Обрезаем изображение
    cropped_img = img.crop((x_offset, y_offset, x_offset + width, y_offset + height))
    # Сохраняем результат
    cropped_img.save(output_path)

# Параметры для обрезки скриншотов
screenshots = [
    {"input_path": "screenshot.png", "output_path": "cropped_first.png", "width": 670, "height": 50, "x_offset": 10, "y_offset": 790},
    {"input_path": "screenshot.png", "output_path": "cropped_first_russian.png", "width": 690, "height": 120, "x_offset": 10, "y_offset": 890},
    {"input_path": "screenshot.png", "output_path": "cropped_second_russian.png", "width": 690, "height": 120, "x_offset": 10, "y_offset": 1000},
    {"input_path": "screenshot.png", "output_path": "cropped_third_russian.png", "width": 690, "height": 120, "x_offset": 10, "y_offset": 1150},
    {"input_path": "screenshot.png", "output_path": "cropped_fourth_russian.png", "width": 690, "height": 120, "x_offset": 10, "y_offset": 1270}
]

# Список для хранения распознанных текстов на русском
russian_texts = []

# Обрабатываем первый скриншот на английском языке
crop_image(screenshots[0]["input_path"], screenshots[0]["output_path"], screenshots[0]["width"], screenshots[0]["height"], screenshots[0]["x_offset"], screenshots[0]["y_offset"])
img = cv2.imread(screenshots[0]["output_path"])
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
text_eng = pytesseract.image_to_string(img, lang='eng').strip().replace("® ", "")

# Добавляем текст с первого скриншота (на английском) в переменную и выводим его
print("Текст со скриншота на английском:")
print(text_eng)

# Обрабатываем остальные скриншоты на русском языке
for screenshot in screenshots[1:]:
    crop_image(screenshot["input_path"], screenshot["output_path"], screenshot["width"], screenshot["height"], screenshot["x_offset"], screenshot["y_offset"])
    img = cv2.imread(screenshot["output_path"])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    text_rus = pytesseract.image_to_string(img, lang='rus').strip()
    russian_texts.append(text_rus)

# Выводим массив распознанных текстов на русском языке
print("\nМассив текстов на русском:")
print(russian_texts)

# Словарь английских слов и их переводов на русский
dictionary = {
    "Handsome": "Статный",
    "SCleaner": "Уборщик",
    "Hat": "Шляпа",
}

# Проверяем, есть ли перевод английского текста в словаре
if text_eng not in dictionary:
    # Если перевода нет, сохраняем скриншот и текстовый файл
    save_failed_screenshot(text_eng, screenshots[0]["input_path"], text_eng)

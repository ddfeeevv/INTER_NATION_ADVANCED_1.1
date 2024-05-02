import cv2
import pytesseract
import numpy as np
from PIL import Image as PILImage
import pyautogui
import os
import time
import subprocess
import difflib
import re

time.sleep(1)

start_time = time.time()

def run_adb_command(command):
    subprocess.run(command, shell=True)

def take_screenshot(output_path):
    screenshot = pyautogui.screenshot()
    screenshot.save(output_path)

def process_first_screenshot(image_path):
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)
    result = cv2.bitwise_and(img, img, mask=mask)
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(binary, lang='eng')
    # Оставляем только буквы и знак тире
    cleaned_text = re.sub(r'[^a-zA-Z-]', '', text)
    return cleaned_text

screenshot_path = 'screenshot.png'

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
    {"input_path": "screenshot.png", "output_path": "cropped_first.png", "width": 540, "height": 120, "x_offset": 10, "y_offset":750},
    {"input_path": "screenshot.png", "output_path": "cropped_first_russian.png", "width": 490, "height": 90, "x_offset": 30, "y_offset": 890},
    {"input_path": "screenshot.png", "output_path": "cropped_second_russian.png", "width": 490, "height": 90, "x_offset": 30, "y_offset": 998},
    {"input_path": "screenshot.png", "output_path": "cropped_third_russian.png", "width": 490, "height": 90, "x_offset": 30, "y_offset": 1106},
    {"input_path": "screenshot.png", "output_path": "cropped_fourth_russian.png", "width": 490, "height": 90, "x_offset": 30, "y_offset": 1214}
]

take_screenshot("screenshot.png")

# Словарь английских слов и их переводов на русский
dictionary = {
    "Tablecloth": "Скатерть",
    "Hat": "Шляпа",
    "Melon": "Дыня",
    "Nurse": "Медсестра",
    "CinnamonRoll": "Булочка с корицей",
    "«Fridge": "Холодильник",
    "Sofa": "Диван",
    "Fried": "Жареный",
    "Restaurant": "Ресторан",
    "Watermelon": "Арбуз",
    "Rooftop": "Крыша",
    "Carpet": "Ковер",
    "Platform": "Платформа",
    "Goodmoming": "Доброе утро",
}

# Список для хранения распознанных текстов на русском
russian_texts = []

# Обрабатываем первый скриншот на английском языке
crop_image(screenshots[0]["input_path"], screenshots[0]["output_path"], screenshots[0]["width"], screenshots[0]["height"], screenshots[0]["x_offset"], screenshots[0]["y_offset"])
img = cv2.imread(screenshots[0]["output_path"])
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Обрабатываем первый скриншот на английском языке
text_eng = process_first_screenshot(screenshots[0]["output_path"])

# Обрабатываем остальные скриншоты на русском языке
for screenshot in screenshots[1:]:
    crop_image(screenshot["input_path"], screenshot["output_path"], screenshot["width"], screenshot["height"], screenshot["x_offset"], screenshot["y_offset"])
    img = cv2.imread(screenshot["output_path"])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    text_rus = pytesseract.image_to_string(img, lang='rus').strip()
    russian_texts.append(text_rus)

# Функция для поиска индекса перевода в массиве russian_texts
def find_translation(word, russian_words):
    if word in dictionary:
        translation = dictionary[word]
        for index, russian_word in enumerate(russian_words):
            seq = difflib.SequenceMatcher(None, translation.lower(), russian_word.lower())
            ratio = seq.ratio()
            if ratio > 0.8:  # Пороговое значение сходства строк
                return index
    return None

# Проверяем перевод слова из словаря и нажимаем соответствующие координаты
translation_index = find_translation(text_eng, russian_texts)

if translation_index is not None:
    if translation_index == 0:
        run_adb_command('adb -s emulator-5554 shell input tap 540 1600')
        time.sleep(0.1)
        run_adb_command('adb -s emulator-5554 shell input tap 540 2500')
    elif translation_index == 1:
        run_adb_command('adb -s emulator-5554 shell input tap 540 1800')
        time.sleep(0.1)
        run_adb_command('adb -s emulator-5554 shell input tap 540 2500')
    elif translation_index == 2:
        run_adb_command('adb -s emulator-5554 shell input tap 540 2000')
        time.sleep(0.1)
        run_adb_command('adb -s emulator-5554 shell input tap 540 2500')
    elif translation_index == 3:
        run_adb_command('adb -s emulator-5554 shell input tap 540 2200')
        time.sleep(0.1)
        run_adb_command('adb -s emulator-5554 shell input tap 540 2500')
else:
    print("Перевод не найден")
    run_adb_command('adb -s emulator-5554 shell input tap 540 1600')
    time.sleep(0.1)
    run_adb_command('adb -s emulator-5554 shell input tap 540 2500')
    save_failed_screenshot(text_eng, screenshot_path, text_eng)

end_time = time.time()

execution_time = end_time - start_time
print(f"Время выполнения скрипта: {execution_time} секунд")

import cv2
import pytesseract
from PIL import Image as PILImage

# Функция для обрезки изображения
def crop_image(input_path, output_path, width, height, x_offset, y_offset):
    img = PILImage.open(input_path)
    # Обрезаем изображение
    cropped_img = img.crop((x_offset, y_offset, x_offset + width, y_offset + height))
    # Сохраняем результат
    cropped_img.save(output_path)

# Параметры для обрезки скриншотов
screenshots = [
    {"input_path": "screenshot.png", "output_path": "cropped_first.png", "width": 690, "height": 50, "x_offset": 10, "y_offset": 740},
    {"input_path": "screenshot.png", "output_path": "cropped_first_russian.png", "width": 690, "height": 120, "x_offset": 10, "y_offset": 870},
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

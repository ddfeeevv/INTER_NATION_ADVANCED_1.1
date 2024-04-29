import cv2
import pytesseract
import pyautogui
from PIL import Image as PILImage

# Функция для создания скриншота экрана ноутбука
def take_screenshot(output_path):
    screenshot = pyautogui.screenshot()
    screenshot.save(output_path)

# Создаем скриншот экрана ноутбука и сохраняем его в файл
screenshot_path = 'screenshot.png'
#take_screenshot(screenshot_path)

# Функция для обрезки изображения
def crop_image(input_path, output_path, width, height, x_offset, y_offset):
    img = PILImage.open(input_path)
    # Обрезаем изображение
    cropped_img = img.crop((x_offset, y_offset, x_offset + width, y_offset + height))
    # Сохраняем результат
    cropped_img.save(output_path)

# Параметры для обрезки первого скриншота
crop_width1 = 240
crop_height1 = 50
x_offset1 = 280
y_offset1 = 750

# Обрезаем первый скриншот
crop_image(screenshot_path, 'cropped_first.png', crop_width1, crop_height1, x_offset1, y_offset1)

# Загружаем скриншот с помощью OpenCV
img = cv2.imread("cropped_first.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Распознаем текст на скриншоте с помощью Tesseract
config = r'--oem 3 -psm 6'
print(pytesseract.image_to_string(img))

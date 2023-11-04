import cv2

# Инициализация пути к папке с изображениями
folder_path = "Datasets/Must_detect/"

# Цикл для инициализации изображений
images = []
for i in range(1, 6):
    image_path = folder_path + f"Detected_{i}.png"
    image = "image_" + f"{i}"
    #image = cv2.imread(image_path)
    image = cv2.imread(image_path)
    images.append(image)

# Проверка результатов
for image in images:
    cv2.imshow("Image", image)
    cv2.waitKey(0)

cv2.destroyAllWindows()








""" import cv2

# Инициализация очень множества изображений с разными именами
images = [cv2.imread(f"image_{i}.jpg") for i in range(100)]

# Пример использования загруженных изображений
for i, image in enumerate(images):
    cv2.imshow(f"Image {i}:", image)

cv2.waitKey(0)
cv2.destroyAllWindows() """
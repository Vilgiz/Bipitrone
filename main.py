import cv2

# Загрузка изображений
image1 = cv2.imread("Datasets/Resize_photo/image_20.jpg")

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

# Создание объекта SIFT
sift = cv2.SIFT_create()

# Нахождение контрольных точек и дескрипторов для первого изображения
keypoints1, descriptors1 = sift.detectAndCompute(image1, None)

# Нахождение контрольных точек и дескрипторов для второго изображения
keypoints2, descriptors2 = sift.detectAndCompute(images[0], None)
keypoints3, descriptors3 = sift.detectAndCompute(images[1], None)
keypoints4, descriptors4 = sift.detectAndCompute(images[2], None)
keypoints5, descriptors5 = sift.detectAndCompute(images[3], None)
keypoints6, descriptors6 = sift.detectAndCompute(images[4], None)

# Создание объекта BFMatcher для сопоставления дескрипторов
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

# Сопоставление дескрипторов первого изображения с остальными
matches2 = bf.match(descriptors1, descriptors2)
matches3 = bf.match(descriptors1, descriptors3)
matches4 = bf.match(descriptors1, descriptors4)
matches5 = bf.match(descriptors1, descriptors5)
matches6 = bf.match(descriptors1, descriptors6)

# Сортировка сопоставлений по расстоянию
matches2 = sorted(matches2, key=lambda x: x.distance)
matches3 = sorted(matches3, key=lambda x: x.distance)
matches4 = sorted(matches4, key=lambda x: x.distance)
matches5 = sorted(matches5, key=lambda x: x.distance)
matches6 = sorted(matches6, key=lambda x: x.distance)

# Отображение первых 10 сопоставлений для каждого изображения на одном изображении
matching_result = cv2.drawMatches(image1, keypoints1, images[0], keypoints2, matches2[:5], None, flags=2)
matching_result = cv2.drawMatches(matching_result, keypoints1, images[1], keypoints3, matches3[:5], None, flags=2)
matching_result = cv2.drawMatches(matching_result, keypoints1, images[2], keypoints4, matches4[:5], None, flags=2)
matching_result = cv2.drawMatches(matching_result, keypoints1, images[3], keypoints5, matches5[:5], None, flags=2)
matching_result = cv2.drawMatches(matching_result, keypoints1, images[4], keypoints6, matches6[:5], None, flags=2)

# Создание окна и отображение результата
cv2.imshow('Matching Result', matching_result)
cv2.waitKey(0)
cv2.destroyAllWindows()
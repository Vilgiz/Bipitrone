import json
import cv2
import numpy as np


class Image:

    def __init__(self, frame):
        self.brightness_factor = 2.0  # TODO Калибровка
        self.saturation_factor = 400  # TODO Калибровка
        self.threshold_1 = 145
        self.threshold_2 = 11
        self.coordinates = []
        self.counters = [] 
        
    def transform_zone(self, frame: np.ndarray) -> np.ndarray:
        """
        Преобразует изображение с использованием матрицы трансформации.

        Args:
            frame (np.ndarray): Входное изображение в формате NumPy.

        Returns:
            np.ndarray: Преобразованное изображение.
        """
        with open('transformation_data.json', 'r') as json_file:
            try:
                data = json.load(json_file)
            except json.JSONDecodeError:
                raise ValueError(
                    "Ошибка при чтении файла с данными трансформации.")

        M = np.array(data.get('M', []))
        maxWidth, maxHeight = data.get('maxWidth', 0), data.get('maxHeight', 0)

        return cv2.warpPerspective(frame, M, (maxWidth, maxHeight))

    def transform_chees(self, frame: np.ndarray) -> np.ndarray:
        """
        Исправляет искажения в изображении, основываясь на данных калибровки.

        Args:
            frame (np.ndarray): Входное изображение в формате NumPy.

        Returns:
            np.ndarray: Исправленное изображение.
        """
        with open('calibration_result.json', 'r') as json_file:
            try:
                data = json.load(json_file)
            except json.JSONDecodeError:
                raise ValueError(
                    "Ошибка при чтении файла с результатами калибровки.")

        camera_matrix = np.array(data.get('camera_matrix', []))
        dist_coefficients = np.array(data.get('dist_coefficients', []))

        return cv2.undistort(frame, camera_matrix, dist_coefficients)

    # TODO добавить калибровку из gui
    def image_correction(self, frame):
        brightened_image = cv2.convertScaleAbs(
            frame, alpha=self.brightness_factor, beta=0)
        hsv_image = cv2.cvtColor(brightened_image, cv2.COLOR_BGR2HSV)
        hsv_image[:, :, 1] = hsv_image[:, :, 1] * self.saturation_factor
        saturated_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        # Применение гауссова размытия для уменьшения шума
        # blurred = cv2.GaussianBlur(
        #     saturated_image, (1, 1), 0)  # TODO Калибровка

        # # Вычисление разности между исходным и размытым изображением
        # sharp = cv2.addWeighted(
        #     blurred, 1.8, blurred, -0.1, 0)      # TODO Калибровка
        return saturated_image

    def detect_contours(self, frame):
        self.GRAY_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, threshold_image = cv2.threshold(
            self.GRAY_frame, self.threshold_1, self.threshold_2, 0)

        # Ищем контуры в пороговом изображении
        contours, _ = cv2.findContours(
            threshold_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # image_with_contours = self.RGB_frame.copy()
        cv2.drawContours(self.GRAY_frame, contours, -1, (0, 255, 0), 1)
        cv2.drawContours(self.painted, contours, -1, (0, 255, 0), 1)
        # Находим центр тяжести и площадь для каждого контура
        for contour in contours:
            # Находим моменты контура
            M = cv2.moments(contour)

            # Находим центр тяжести
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0

            # Находим площадь контура
            area = cv2.contourArea(contour)
            if area < 100 or area > 1000:
                continue

            # Рисуем маркер для центра тяжести
            cv2.circle(self.GRAY_frame, (cX, cY), 2, (255, 0, 0), -1)
            cv2.circle(self.painted, (cX, cY), 2, (0, 0, 255), -1)

            # Пишем площадь рядом с контуром
            cv2.drawContours(self.GRAY_frame, contour, -1, (0, 255, 0), -1)
            self.counters.append(contour)

            rect = cv2.minAreaRect(contour)

            # Извлечь угол наклона из параметров прямоугольника
            angle = rect[2]

            # Отобразить изображение с контуром и углом наклона
            self.painted = cv2.drawContours(
                self.painted, [contour], -1, 255, 2)
            self.painted = cv2.putText(self.painted, f"tilt angle: {angle:.2f}", (cX - 20, cY - 20),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1, cv2.LINE_AA)
            """ cv2.putText(self.GRAY_frame, f"Area: {area}", (
                cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(self.GRAY_frame, f"Coord: {cX, cY}", (
                cX - 20, cY + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2) """

            """ cv2.putText(self.painted, f"Area: {area}", (cX - 20, cY - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            cv2.putText(self.painted, f"Coord: {cX, cY}", (
                cX - 20, cY + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2) """
            self.coordinates.append([cX, cY])

        print(f"Обнаружено деталей: {len(self.coordinates)}")
        print(f"Координаты: {self.coordinates}")
        return self.painted

    def draw_contours(self):
        pass

    def prepare_frames(self, frame):
        self.frame = frame
        self.RGB_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.GRAY_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.HSV_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.painted = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

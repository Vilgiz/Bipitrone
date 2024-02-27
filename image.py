import json
import cv2
import numpy as np
from part import Part
import gc


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

    def image_correction(self, frame):
        brightened_image = cv2.convertScaleAbs(
            frame, alpha=self.brightness_factor, beta=0)
        hsv_image = cv2.cvtColor(brightened_image, cv2.COLOR_BGR2HSV)
        hsv_image[:, :, 1] = hsv_image[:, :, 1] * self.saturation_factor
        saturated_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        # Применение гауссова размытия для уменьшения шума
        blurred = cv2.GaussianBlur(
            saturated_image, (1, 1), 0)  # TODO Калибровка

        # # Вычисление разности между исходным и размытым изображением
        # sharp = cv2.addWeighted(
        #     blurred, 1.8, blurred, -0.1, 0)      # TODO Калибровка
        return saturated_image

    def detect_contours(self, frame):
        self.centers = []
        self.angels = []
        GRAY_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # _, threshold_image = cv2.threshold(
        #     GRAY_frame, self.threshold_1, self.threshold_2, 0)

        # self.contours, _ = cv2.findContours(
        #     threshold_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # # ! cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)

        WHITE_frame = cv2.imread("Prepared_Image/white.jpg")

        edges = cv2.Canny(GRAY_frame, self.threshold_1, self.threshold_2)
        self.contours, hierarchy = cv2.findContours(
            edges, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(frame, self.contours, -1, (0, 255, 0), 1)
        cv2.drawContours(WHITE_frame, self.contours, -1,
                         (0, 0, 255), thickness=3)  # TODO ТУТ ЕСТЬ ПАРАМЕТР КАЛИБРОВКИ!

        WHITE_frame = cv2.GaussianBlur(WHITE_frame, (7, 7), 0)
        cv2.imshow("ere_2", WHITE_frame)
        WHITE_frame = cv2.cvtColor(WHITE_frame, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(WHITE_frame, self.threshold_1, self.threshold_2)
        self.contours, hierarchy = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(WHITE_frame, self.contours, -1,
                         (255, 255, 255), thickness=cv2.FILLED)

        self.parts = []
        for contour in self.contours:
            M = cv2.moments(contour)

            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0

            # Находим площадь контура
            area = cv2.contourArea(contour)
            if area < 100 or area > 800:
                continue

            self.centers.append((cX, cY))
            self.counters.append(contour)

            rect = cv2.minAreaRect(contour)
            # Извлечь угол наклона из параметров прямоугольника
            angle = rect[2]
            self.angels.append(angle)

            cv2.putText(frame, f"Area: {area}", (cX - 20, cY - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1)

            self.coordinates.append([cX, cY])
            cv2.putText(frame, f"{len(self.coordinates)}",
                        (cX, cY), 1, 2, (0, 0, 0), 2)
            self.part_type_definition(
                cX, cY, angle, area, number=len(self.coordinates))
        print(len(self.parts))
        return frame, self.coordinates

    def draw_contours(self, frame):
        cv2.drawContours(frame, self.contours, -1, (0, 255, 0), 1)
        for center, contour, angle in zip(self.coordinates, self.counters, self.angels):
            cv2.circle(frame, tuple(center), 2, (0, 0, 255), -1)
            frame = cv2.drawContours(frame, [contour], -1, 255, 1)
            # frame = cv2.putText(frame, f"tilt angle: {angle:.2f}", (center[0] - 20, center[1] - 20),
            #                     cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1, cv2.LINE_AA)

        # print(f"Обнаружено деталей: {len(self.coordinates)}")
        # print(f"Координаты: {self.coordinates}")

        return frame

    def prepare_frames(self, frame):
        self.frame = frame
        self.RGB_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.GRAY_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.HSV_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.painted = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

    def part_type_definition(self, cX, cY, angle, area, number):
        # if area < 600 and area > 420:
        #     print("Type 4, 5")
        # elif area < 220 and area > 160:
        #     print("Type 3")
        # elif area < 310 and area > 250:
        #     print("Type 2")
        # elif area < 150 and area > 100:
        #     print("Type 1")
        
        part = Part(cX, cY, angle, area, number)
        self.parts.append(part)
        

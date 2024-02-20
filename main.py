import cv2
import numpy
import cvzone
from pypylon import pylon
import numpy as np
import cv2.aruco as aruco
import json
import asyncio
from camera import Camera

asyncio

# async def


class vision_billet:

    def __init__(self) -> None:

        self.brightness_factor = 3000
        self.saturation_factor = 2000

        self.circles_min_array = []
        self.circles_max_array = []

        self.counters = []
        self.coordinates = []

        self.threshold_1 = 295
        self.threshold_2 = 1
        self.minRadius = 20
        self.maxRadius = 30

        self.activate = False

    def prepare_frames(self, frame):

        self.frame = frame
        self.original = frame
        self.WHITE_frame = cv2.imread("Prepared_Image/white.jpg")
        self.RGB_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.GRAY_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.HSV_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.painted = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        height_W, width_W, _ = self.WHITE_frame.shape
        height, width, _ = self.frame.shape
        width = (width/width_W)
        height = (height/height_W)
        self.WHITE_frame = cv2.resize(
            self.WHITE_frame, None, fx=width, fy=height)

    def detect_contours(self):
        # self.threshold_2 = (self.threshold_2+1)/100
        # maxRadius = self.maxRadius
        # minRadius = self.minRadius
        # circles_min = cv2.HoughCircles(self.GRAY_frame, cv2.HOUGH_GRADIENT_ALT, 1, 75,
        #                                param1=self.threshold_1, param2=self.threshold_2,
        #                                minRadius=0, maxRadius=12)
        # circles_max = cv2.HoughCircles(self.GRAY_frame, cv2.HOUGH_GRADIENT_ALT, 1, 75,
        #                                param1=self.threshold_1, param2=self.threshold_2,
        #                                minRadius=minRadius, maxRadius=maxRadius)

        # if circles_min is not None:
        #     circles_min = np.uint16(np.around(circles_min))
        #     red_circles = []
        #     for i in circles_min[0, :]:
        #         red_circles.append((i[0], i[1], i[2]))
        #     for circle in red_circles:
        #         self.radius_cv = int(circle[2])
        #         x_cv = circle[0]
        #         y_cv = circle[1]
        #         self.center_cv = (x_cv, y_cv)
        #         cv2.circle(self.painted, (x_cv, y_cv),
        #                    self.radius_cv, (0, 255, 0), 1)

        #         self.circles_min_array.append((int(x_cv), int(y_cv)))

        # if circles_max is not None:
        #     circles_max = np.uint16(np.around(circles_max))
        #     red_circles = []
        #     for i in circles_max[0, :]:
        #         red_circles.append((i[0], i[1], i[2]))
        #     for circle in red_circles:
        #         self.radius_cv = int(circle[2])
        #         x_cv = circle[0]
        #         y_cv = circle[1]
        #         self.center_cv = (x_cv, y_cv)
        #         self.circles_max_array.append((int(x_cv), int(y_cv)))
        #         cv2.circle(self.painted, (x_cv, y_cv),
        #                    self.radius_cv, (0, 0, 255), 1)

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

    def __check_blillet(self):
        pass

    def color_correction(self, frame):

        brightened_image = cv2.convertScaleAbs(
            frame, alpha=self.brightness_factor, beta=0)

        hsv_image = cv2.cvtColor(brightened_image, cv2.COLOR_BGR2HSV)
        hsv_image[:, :, 1] = hsv_image[:, :, 1] * self.saturation_factor
        self.saturated_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        return self.saturated_image

    def show_video(self, resize_coff):
        ImgList = [self.original, self.HSV_frame, self.GRAY_frame,
                   self.painted]  # TODO Параметр калибровки - ImgList
        # ImgList = [self.painted]
        # TODO Параметр калибровки - cols, scale
        stackedImg = cvzone.stackImages(ImgList, cols=2, scale=2)

        height, width, _ = self.frame.shape
        width = int(width/resize_coff)
        height = int(height/resize_coff)

        cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Video', width, height)
        cv2.imshow("Video", stackedImg)

    def activate_sliders(self):
        cv2.createTrackbar('threshold_1', 'Video', 1, 1000, self.__pass)
        cv2.createTrackbar('threshold_2', 'Video', 1, 100, self.__pass)

        cv2.createTrackbar('minRadius', 'Video', 1, 100, self.__pass)
        cv2.createTrackbar('maxRadius', 'Video', 1, 100, self.__pass)

        cv2.createTrackbar('brightness_factor', 'Video', 1, 3000, self.__pass)
        cv2.createTrackbar('saturation_factor', 'Video', 1, 2000, self.__pass)

        self.activate = True

    def get_sliders(self):
        if self.activate is True:
            threshold_1 = cv2.getTrackbarPos('threshold_1', 'Video')
            threshold_2 = cv2.getTrackbarPos('threshold_2', 'Video')

            minRadius = cv2.getTrackbarPos('minRadius', 'Video')
            maxRadius = cv2.getTrackbarPos('maxRadius', 'Video')

            brightness_factor = cv2.getTrackbarPos(
                'brightness_factor', 'Video')
            saturation_factor = cv2.getTrackbarPos(
                'saturation_factor', 'Video')
            self.__function_sliders(
                threshold_1, threshold_2, brightness_factor, saturation_factor, minRadius, maxRadius)

    def __function_sliders(self, threshold_1, threshold_2, brightness_factor, saturation_factor, minRadius, maxRadius):
        self.threshold_1 = threshold_1
        self.threshold_2 = threshold_2

        self.maxRadius = maxRadius
        self.minRadius = minRadius

        self.brightness_factor = brightness_factor / 1000
        self.saturation_factor = saturation_factor / 1000

    def __pass(self, df):
        pass

    def tranform(self, frame):
        with open('transformation_data.json', 'r') as json_file:

            data = json.load(json_file)

        M = np.array(data['M'])
        maxWidth = data['maxWidth']
        maxHeight = data['maxHeight']
        frame = cv2.warpPerspective(
            frame, M, (maxWidth, maxHeight))

        with open('calibration_result.json', 'r') as json_file:
            data = json.load(json_file)

        camera_matrix = np.array(data['camera_matrix'])
        dist_coefficients = np.array(data['dist_coefficients'])

        frame = cv2.undistort(
            frame, camera_matrix, dist_coefficients)
        return frame


if __name__ == '__main__':

    vision = vision_billet()
    camera = Camera()

    while True:
        vision.coordinates = []

        frame = camera.get_image()

        frame = vision.tranform(frame)
        frame = vision.color_correction(frame)

        vision.prepare_frames(frame)
        vision.detect_contours()

        vision.show_video(0.8)
        vision.get_sliders()

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('k'):
            vision.activate_sliders()

camera.end()

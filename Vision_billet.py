
import cv2
import numpy
import cvzone

import asyncio

asyncio

#async def

class Calibration_Vision:
    def __init__(self) -> None:
        pass

class Vision_billet:

    def __init__(self) -> None:
        self.frame = None
        self.original = None
        self.brightness_factor = 3000
        self.saturation_factor = 2000

        self.threshold_1 = 295                       
        self.threshold_2 = 846

        self.activate = False

        folder_path = "Datasets/Must_detect/"

        self.images = []
        for i in range(1, 14):
            image_path = folder_path + f"Detected_{i}.png"
            image = cv2.imread(image_path)
            self.images.append(image)


    def __prepare_video(self):
        self.RGB_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.GRAY_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.HSV_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

        self.WHITE_frame = cv2.imread("Prepared_Image/white.jpg")                       ###  * Временное решение, не забыть убрать
        height_W, width_W, _ = self.WHITE_frame.shape                                   ###  * Временное решение, не забыть убрать
        height, width, _ = self.frame.shape                                             ###  * Временное решение, не забыть убрать
        width = (width/width_W)                                                         ###  * Временное решение, не забыть убрать
        height = (height/height_W)                                                      ###  * Временное решение, не забыть убрать
        self.WHITE_frame = cv2.resize(self.WHITE_frame, None, fx=width, fy=height)      ###  * Временное решение, не забыть убрать


    def __detect_contours(self):
        """ frame = self.GRAY_frame
        _, threshold = cv2.threshold(self.GRAY_frame, self.threshold_1, self.threshold_2, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        edges = cv2.Canny(self.GRAY_frame, self.threshold_1, self.threshold_2)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        cv2.drawContours(self.WHITE_frame, contours, -1, (0, 255, 0), 2) """

        # Создание объекта SIFT
        sift = cv2.SIFT_create()

        # Нахождение контрольных точек и дескрипторов для первого изображения
        keypoints1, descriptors1 = sift.detectAndCompute(self.frame, None)

        # Нахождение контрольных точек и дескрипторов для второго изображения
        keypoints2, descriptors2 = sift.detectAndCompute(self.images[0], None)
        keypoints3, descriptors3 = sift.detectAndCompute(self.images[1], None)
        keypoints4, descriptors4 = sift.detectAndCompute(self.images[2], None)
        keypoints5, descriptors5 = sift.detectAndCompute(self.images[3], None)
        keypoints6, descriptors6 = sift.detectAndCompute(self.images[4], None)
        keypoints7, descriptors7 = sift.detectAndCompute(self.images[5], None)
        keypoints8, descriptors8 = sift.detectAndCompute(self.images[6], None)
        keypoints9, descriptors9 = sift.detectAndCompute(self.images[7], None)
        keypoints10, descriptors10 = sift.detectAndCompute(self.images[8], None)
        keypoints11, descriptors11 = sift.detectAndCompute(self.images[9], None)
        keypoints12, descriptors12 = sift.detectAndCompute(self.images[10], None)

        # Создание объекта BFMatcher для сопоставления дескрипторов
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

        # Сопоставление дескрипторов первого изображения с остальными
        matches2 = bf.match(descriptors1, descriptors2)
        matches3 = bf.match(descriptors1, descriptors3)
        matches4 = bf.match(descriptors1, descriptors4)
        matches5 = bf.match(descriptors1, descriptors5)
        matches6 = bf.match(descriptors1, descriptors6)
        matches7 = bf.match(descriptors1, descriptors7)
        matches8 = bf.match(descriptors1, descriptors8)
        matches9 = bf.match(descriptors1, descriptors9)
        matches10 = bf.match(descriptors1, descriptors10)
        matches11 = bf.match(descriptors1, descriptors11)
        matches12 = bf.match(descriptors1, descriptors12)

        # Сортировка сопоставлений по расстоянию
        matches2 = sorted(matches2, key=lambda x: x.distance)
        matches3 = sorted(matches3, key=lambda x: x.distance)
        matches4 = sorted(matches4, key=lambda x: x.distance)
        matches5 = sorted(matches5, key=lambda x: x.distance)
        matches6 = sorted(matches6, key=lambda x: x.distance)
        matches7 = sorted(matches7, key=lambda x: x.distance)
        matches8 = sorted(matches8, key=lambda x: x.distance)
        matches9 = sorted(matches9, key=lambda x: x.distance)
        matches10 = sorted(matches10, key=lambda x: x.distance)
        matches11 = sorted(matches11, key=lambda x: x.distance)
        matches12 = sorted(matches12, key=lambda x: x.distance)

        # Отображение первых 10 сопоставлений для каждого изображения на одном изображении
        matching_result = cv2.drawMatches(self.frame, keypoints1, self.images[0], keypoints2, matches2[:1], None, flags=2)
        matching_result = cv2.drawMatches(matching_result, keypoints1, self.images[1], keypoints3, matches3[:1], None, flags=2)
        matching_result = cv2.drawMatches(matching_result, keypoints1, self.images[2], keypoints4, matches4[:1], None, flags=2)
        matching_result = cv2.drawMatches(matching_result, keypoints1, self.images[3], keypoints5, matches5[:1], None, flags=2)
        matching_result = cv2.drawMatches(matching_result, keypoints1, self.images[4], keypoints6, matches6[:1], None, flags=2)
        matching_result = cv2.drawMatches(matching_result, keypoints1, self.images[5], keypoints7, matches7[:1], None, flags=2)
        matching_result = cv2.drawMatches(matching_result, keypoints1, self.images[6], keypoints8, matches8[:1], None, flags=2)
        matching_result = cv2.drawMatches(matching_result, keypoints1, self.images[7], keypoints9, matches9[:1], None, flags=2)
        matching_result = cv2.drawMatches(matching_result, keypoints1, self.images[8], keypoints10, matches10[:1], None, flags=2)
        matching_result = cv2.drawMatches(matching_result, keypoints1, self.images[9], keypoints11, matches11[:1], None, flags=2)
        self.WHITE_frame = cv2.drawMatches(matching_result, keypoints1, self.images[10], keypoints12, matches12[:1], None, flags=2)


    def find_billet(self):
        self.__prepare_video()                        ###  !!! СУКА ПЕРЕДЕЛАЙ ЭТО ГОВНО!
        self.__detect_contours()

    def __check_blillet(self):
        pass

    def color_correction(self, frame):

        brightened_image = cv2.convertScaleAbs(frame, alpha=self.brightness_factor, beta=0)

        hsv_image = cv2.cvtColor(brightened_image, cv2.COLOR_BGR2HSV)
        hsv_image[:, :, 1] = hsv_image[:, :, 1] * self.saturation_factor
        self.saturated_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)                       ###  * Временное решение, не забыть убрать
        return self.saturated_image                       ###  * Временное решение, не забыть убрать


    def show_video(self, resize_coff):
        ImgList = [self.original, self.HSV_frame, self.GRAY_frame, self.WHITE_frame]                       ###  TODO Параметр калибровки - ImgList                                            
        stackedImg = cvzone.stackImages(ImgList, cols = 2, scale = 1)                 ###  TODO Параметр калибровки - cols, scale

        height, width, _ = self.frame.shape
        width = int(width/resize_coff)
        height = int(height/resize_coff)
        
        cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Video', width, height)         
        cv2.imshow("Video", stackedImg)

    def activate_sliders(self):
        cv2.createTrackbar('threshold_1', 'Video', 1, 1000, self.__pass)
        cv2.createTrackbar('threshold_2', 'Video', 1, 2000, self.__pass)

        cv2.createTrackbar('brightness_factor', 'Video', 1, 3000, self.__pass)
        cv2.createTrackbar('saturation_factor', 'Video', 1, 2000, self.__pass)

        self.activate = True

    def get_sliders(self):
        if self.activate is True:  
            threshold_1 = cv2.getTrackbarPos('threshold_1', 'Video')
            threshold_2 = cv2.getTrackbarPos('threshold_2', 'Video')

            brightness_factor = cv2.getTrackbarPos('brightness_factor', 'Video')
            saturation_factor = cv2.getTrackbarPos('saturation_factor', 'Video')
            self.__function_sliders(threshold_1, threshold_2, brightness_factor, saturation_factor)
    
    def __function_sliders(self, threshold_1, threshold_2, brightness_factor, saturation_factor):
        self.threshold_1 = threshold_1
        self.threshold_2 = threshold_2

        self.brightness_factor = brightness_factor / 1000
        self.saturation_factor = saturation_factor / 1000
    
    def __pass(self, df):
        pass
    


if __name__ == '__main__':

    video = cv2.VideoCapture(0)
    video = cv2.VideoCapture("Datasets/video_13.mp4")
    Vision = Vision_billet()
    Calibration = Calibration_Vision()


    while (True):

        ret, frame = video.read()
        if not ret:
            break
        #frame = cv2.imread("Datasets/Resize_photo/image_32.jpg")          
        Vision.original = frame
        frame = Vision.color_correction(frame)
        Vision.frame = frame
        




        Vision.find_billet()
        Vision.show_video(2)               ### TODO Параметр калибровки - (0.67) (2) (0.8) (1.2)   
        Vision.get_sliders()   
           

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('k'):
            Vision.activate_sliders()

video.release()
cv2.destroyAllWindows()

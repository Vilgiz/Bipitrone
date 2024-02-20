
import cv2
import cvzone

import asyncio

#async def

class Calibration_Vision:
    def __init__(self) -> None:
        pass

class Vision_billet:
    
    

    def __init__(self) -> None:
        self.frame = None
        self.original = None
        self.painted = self.original
        self.brightness_factor = 580
        self.saturation_factor = 1040

        self.threshold_1 = 127                       
        self.threshold_2 = 255

        self.activate = False

        folder_path = "Datasets/Must_detect/"

        self.images = []
        
        for i in range(1, 14):
            image_path = folder_path + f"Detected_{i}.png"
            image = cv2.imread(image_path)
            self.images.append(image)
            
        self.counters = []
        self.coordinates = []


    def __prepare_video(self):
        self.RGB_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.GRAY_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.HSV_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        self.painted = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        self.WHITE_frame = cv2.imread("Prepared_Image/white.jpg")                       ###  * Временное решение, не забыть убрать
        height_W, width_W, _ = self.WHITE_frame.shape                                   ###  * Временное решение, не забыть убрать
        height, width, _ = self.frame.shape                                             ###  * Временное решение, не забыть убрать
        width = (width/width_W)                                                         ###  * Временное решение, не забыть убрать
        height = (height/height_W)                                                      ###  * Временное решение, не забыть убрать
        self.WHITE_frame = cv2.resize(self.WHITE_frame, None, fx=width, fy=height)      ###  * Временное решение, не забыть убрать


    def __detect_contours(self):

        _, threshold_image = cv2.threshold(self.GRAY_frame, self.threshold_1, self.threshold_2, 0)

        # Ищем контуры в пороговом изображении
        contours, _ = cv2.findContours(threshold_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #image_with_contours = self.RGB_frame.copy()
        cv2.drawContours(self.GRAY_frame, contours, -1, (0, 255, 0), 3)
        cv2.drawContours(self.painted, contours, -1, (0, 255, 0), 3)
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
            if area < 1000 or area > 10000:
                continue

            # Рисуем маркер для центра тяжести
            cv2.circle(self.GRAY_frame, (cX, cY), 5, (255, 0, 0), -1)
            cv2.circle(self.painted, (cX, cY), 5, (0, 0, 255), -1)

            # Пишем площадь рядом с контуром
            cv2.drawContours(self.GRAY_frame, contour, -1, (0, 255, 0), -1)
            self.counters.append(contour)
            cv2.putText(self.GRAY_frame, f"Area: {area}", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
            cv2.putText(self.GRAY_frame, f"Coord: {cX, cY}", (cX - 20, cY + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
            
            cv2.putText(self.painted, f"Area: {area}", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)
            cv2.putText(self.painted, f"Coord: {cX, cY}", (cX - 20, cY + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
            self.coordinates.append([cX,cY])
            
        print(f"Обнаружено деталей: {len(self.coordinates)}")
        pass

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
        self.saturated_image = cv2.GaussianBlur(self.saturated_image, (5, 5), 0)    
        return self.saturated_image                       ###  * Временное решение, не забыть убрать


    def show_video(self, resize_coff):
        ImgList = [self.painted, self.GRAY_frame]                       ###  TODO Параметр калибровки - ImgList                                            
        #ImgList = [self.GRAY_frame]
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

    video = cv2.VideoCapture(1)
    #video = cv2.VideoCapture("Datasets/video_16.mp4")
    Vision = Vision_billet()
    Calibration = Calibration_Vision()


    while (True):

        ret, frame = video.read()
        if not ret:
            break
        #frame = cv2.imread("Datasets/Resize_photo/image_36.png")          
        Vision.original = frame
        frame = Vision.color_correction(frame)
        Vision.frame = frame
        
        Vision.find_billet()
        Vision.show_video(1.5)               ### TODO Параметр калибровки - (0.67) (2) (0.8) (1.2)   
        Vision.get_sliders()   
        Vision.coordinates = []
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('k'):
            Vision.activate_sliders()

video.release()
cv2.destroyAllWindows()

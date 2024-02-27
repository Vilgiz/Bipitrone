import sys
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QSlider
import cv2
from PyQt6.QtCore import Qt
import json
from image import Image
from camera import Camera
from robot import Robot


class VideoPlayer(QMainWindow):

    def __init__(self):
        super().__init__()
        self.camera = Camera()
        self.robot = Robot()
        self.width_frame = None
        self.height_frame = None

        self.brigh_fac_value = 0
        self.sat_fac_value = 0
        self.threshold_1_value = 0
        self.threshold_2_value = 0

        self.start_flag = True

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(10)  # Обновление каждые 10 миллисекунд

        self.__init_main_window()
        self.__init_layouts()
        self.__init_widgets()
        self.__init_style()
        self.__init_sizes()
        self.__addition_widgets()
        self.__setting_layers()
        self.__settings()

    def __init_main_window(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Video")
        self.resize(600, 600)
        self.setStyleSheet("background-color: rgba(255, 255, 255, 150);")

    def __init_widgets(self):
        self.video_label = QLabel()

        self.brigh_fac_slider = QSlider(objectName="brigh_fac_slider")
        self.sat_fac_slider = QSlider(objectName="sat_fac_slider")
        self.threshold_1_slider = QSlider(objectName="threshold_1_slider")
        self.threshold_2_slider = QSlider(objectName="threshold_2_slider")

        self.brigh_fac_label = QLabel("Яркость")
        self.sat_fac_label = QLabel("Насыщение")
        self.threshold_1_label = QLabel(
            "Настройка чувствительность обнаружения № 1")
        self.threshold_2_label = QLabel(
            "Настройка чувствительность обнаружения № 2")
        self.detect_detail_label = QLabel("Обнаружено деталей:")

    def __init_layouts(self):
        self.main_layout = QHBoxLayout(self.central_widget)
        self.video_and_info_layout = QHBoxLayout()
        self.video_layout = QVBoxLayout()
        self.info_layout = QVBoxLayout()
        self.vid_info_and_dop_layout = QVBoxLayout()
        self.dop_layout = QHBoxLayout()
        self.calibration_layout = QVBoxLayout()

    def __addition_widgets(self):
        self.video_layout.addWidget(self.video_label)

        self.calibration_layout.addWidget(self.brigh_fac_label)
        self.calibration_layout.addWidget(self.brigh_fac_slider)
        self.calibration_layout.addWidget(self.sat_fac_label)
        self.calibration_layout.addWidget(self.sat_fac_slider)
        self.calibration_layout.addWidget(self.threshold_1_label)
        self.calibration_layout.addWidget(self.threshold_1_slider)
        self.calibration_layout.addWidget(self.threshold_2_label)
        self.calibration_layout.addWidget(self.threshold_2_slider)

        self.info_layout.addWidget(self.detect_detail_label)

    def __setting_layers(self):
        self.video_and_info_layout.addLayout(self.video_layout)
        self.video_and_info_layout.addLayout(self.info_layout)
        self.vid_info_and_dop_layout.addLayout(self.video_and_info_layout)
        self.vid_info_and_dop_layout.addLayout(self.dop_layout)
        self.main_layout.addLayout(self.vid_info_and_dop_layout)
        self.main_layout.addLayout(self.calibration_layout)

    def __settings(self):
        self.slider_label_mapping = {
            self.brigh_fac_slider: self.brigh_fac_label,
            self.sat_fac_slider: self.sat_fac_label,
            self.threshold_1_slider: self.threshold_1_label,
            self.threshold_2_slider: self.threshold_2_label
        }

        for slider, label in self.slider_label_mapping.items():
            slider.setOrientation(Qt.Orientation.Horizontal)
            slider.setMinimum(0)
            slider.setMaximum(255)
            slider.valueChanged.connect(self.on_slider_value_changed)
            
        if self.start_flag:
            with open('video_parametrs.json', 'r') as json_file:
                try:
                    data = json.load(json_file)
                except json.JSONDecodeError:
                    raise ValueError(
                        "Ошибка при чтении файла с данными.")
            self.brigh_fac_value = data.get('brigh', [])  # TODO - плохо выглядит
            self.sat_fac_value = data.get('sat', []) # TODO - плохо выглядит
            self.threshold_1_value = data.get('threshold_1', []) # TODO - плохо выглядит
            self.threshold_2_value = data.get('threshold_2', []) # TODO - плохо выглядит
            
            self.brigh_fac_slider.setValue(int(self.brigh_fac_value*255/3)) # TODO - плохо выглядит
            self.sat_fac_slider.setValue(self.sat_fac_value) # TODO - плохо выглядит
            self.threshold_1_slider.setValue(self.threshold_1_value) # TODO - плохо выглядит
            self.threshold_2_slider.setValue(self.threshold_2_value) # TODO - плохо выглядит
            self.start_flag = False


    def __init_style(self):
        pass

    def __init_sizes(self):
        frame = self.camera.get_image()
        image = Image(frame)
        frame = image.transform_zone(frame)
        frame = image.transform_chees(frame)
        frame = image.image_correction(frame)
        self.height_frame, self.width_frame, _ = frame.shape
        self.video_label.setMinimumSize(
            int(self.width_frame*2), int(self.height_frame*2)) # TODO Костыль 

    def update_frame(self):
        frame = self.camera.get_image()
        self.image = Image(frame)

        self.image.brightness_factor = self.brigh_fac_value   # TODO - Это костыль,
        self.image.saturation_factor = self.sat_fac_value     # TODO переобозначаю значения
        self.image.threshold_1 = self.threshold_1_value       # TODO калибров чтобы данные
        self.image.threshold_2 = self.threshold_2_value
        # TODO брал из gui при соз

        frame = self.image.transform_zone(frame)
        frame = self.image.transform_chees(frame)
        frame = self.image.image_correction(frame)
        frame, coordinates = self.image.detect_contours(frame)
        frame = self.image.draw_contours(frame)
        frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)

        # Преобразование изображения OpenCV в формат QImage
        self.height_frame, self.width_frame, _ = frame.shape
        bytes_per_line = 3 * self.width_frame  # Для RGB888 (3 канала)
        q_image = QImage(frame.data, self.width_frame, self.height_frame,
                         bytes_per_line, QImage.Format.Format_BGR888)

        # Отображение изображения в QLabel
        self.video_label.setPixmap(QPixmap.fromImage(q_image))
        self.detect_detail_label.setText(
            f"Обнаружено деталей: {len(coordinates)}")
        
        try:
            self.robot.open_socket()
            self.robot.cast_message("move", f"{coordinates[0][1]+27}", f"{coordinates[0][0]-13};")
            self.robot.send_message(self.robot.message)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        finally:
            self.robot.close_socket()

    def closeEvent(self, event):
        self.camera.end()
        event.accept()

    def on_slider_value_changed(self, value):
        if self.start_flag == True:
            return 0
        sender_slider = self.sender()

        corresponding_label = self.slider_label_mapping.get(sender_slider)

        if sender_slider == self.brigh_fac_slider:
            self.brigh_fac_value = value/255*3
            description = "Яркость"
        elif sender_slider == self.sat_fac_slider:
            self.sat_fac_value = value
            description = "Насыщение"
        elif sender_slider == self.threshold_1_slider:
            self.threshold_1_value = value
            description = "Настройка чувствительность обнаружения № 1"
        elif sender_slider == self.threshold_2_slider:
            self.threshold_2_value = value+1
            description = "Настройка чувствительность обнаружения № 2"

        if corresponding_label is not None:
            corresponding_label.setText(f"{description}: {value}")

        data = {
            'brigh': self.brigh_fac_value,
            'sat': self.sat_fac_value,
            'threshold_1': self.threshold_1_value,
            'threshold_2': self.threshold_2_value
        }
        with open('video_parametrs.json', 'w') as json_file:
            json.dump(data, json_file)

        self.image.brightness_factor = self.brigh_fac_value     # TODO - плохо выглядит
        self.image.saturation_factor = self.sat_fac_value       # TODO - плохо выглядит
        self.image.threshold_1 = self.threshold_1_value         # TODO - плохо выглядит
        self.image.threshold_2 = self.threshold_2_value         # TODO - плохо выглядит


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())

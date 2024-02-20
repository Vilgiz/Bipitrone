import sys
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QSlider
import cv2
from PyQt6.QtCore import Qt

from image import Image
from camera import Camera


class VideoPlayer(QMainWindow):

    def __init__(self):
        super().__init__()
        self.camera = Camera()
        self.width_frame = None
        self.height_frame = None

        self.brigh_fac_value = 0
        self.sat_fac_value = 0
        self.threshold_1_value = 0
        self.threshold_2_value = 0

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

        self.brigh_fac_slider = QSlider()
        self.sat_fac_slider = QSlider()
        self.threshold_1_slider = QSlider()
        self.threshold_2_slider = QSlider()

        self.brigh_fac_label = QLabel("Яркость")
        self.sat_fac_label = QLabel("Насыщение")
        self.threshold_1_label = QLabel(
            "Настройка чувствительность обнаружения № 1")
        self.threshold_2_label = QLabel(
            "Настройка чувствительность обнаружения № 2")

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
            int(self.width_frame), int(self.height_frame))

    def update_frame(self):
        frame = self.camera.get_image()
        self.image = Image(frame)
        self.image.brightness_factor = self.brigh_fac_value   # TODO - Это костыль,
        self.image.saturation_factor = self.sat_fac_value     # TODO переобозначаю значения
        self.image.threshold_1 = self.threshold_1_value       # TODO калибров чтобы данные
        # TODO брал из gui при соз
        self.image.threshold_2 = self.threshold_2_value       # TODO IMAGE
        frame = self.image.transform_zone(frame)
        frame = self.image.transform_chees(frame)
        frame = self.image.image_correction(frame)
        # TODO не работает отображение
        cv2.imshow("ef", frame)
        self.image.prepare_frames(frame)
        fmame_paint = self.image.detect_contours(frame)

        # Изменение размера кадра до размера QLabel
        fmame_paint = cv2.resize(
            frame, (self.video_label.width(), self.video_label.height()))

        self.camera.show(fmame_paint)
        # Преобразование изображения OpenCV в формат QImage
        self.height_frame, self.width_frame, _ = fmame_paint.shape
        bytes_per_line = 3 * self.width_frame  # Для RGB888 (3 канала)
        q_image = QImage(fmame_paint.data, self.width_frame, self.height_frame,
                         bytes_per_line, QImage.Format.Format_RGB888)

        # Отображение изображения в QLabel
        self.video_label.setPixmap(QPixmap.fromImage(q_image))

    def closeEvent(self, event):
        self.camera.end()
        event.accept()

    def on_slider_value_changed(self, value):
        sender_slider = self.sender()

        # Получите соответствующую метку из словаря
        corresponding_label = self.slider_label_mapping.get(sender_slider)

        if sender_slider == self.brigh_fac_slider:
            self.brigh_fac_value = value
        elif sender_slider == self.sat_fac_slider:
            self.sat_fac_value = value
        elif sender_slider == self.threshold_1_slider:
            self.threshold_1_value = value
        elif sender_slider == self.threshold_2_slider:
            self.threshold_2_value = value

        if corresponding_label is not None:
            corresponding_label.setText(f"Значение: {value}")

        self.image.brightness_factor = self.brigh_fac_value     # TODO - плохо выглядит
        self.image.saturation_factor = self.sat_fac_value       # TODO - плохо выглядит
        self.image.threshold_1 = self.threshold_1_value         # TODO - плохо выглядит
        self.image.threshold_2 = self.threshold_2_value         # TODO - плохо выглядит


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec())

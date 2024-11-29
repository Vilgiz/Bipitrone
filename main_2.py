import cv2
from image import Image
from camera import Camera


if __name__ == '__main__':
    camera = Camera()

    while True:
        frame = camera.get_image()

        image = Image(frame)
        frame = image.transform_zone(frame)
        # frame = image.transform_chees(frame)
        frame = image.image_correction(frame)
        # image.prepare_frames(frame)
        frame_painted, __, __ = image.detect_contours(frame)
        # frame_painted = image.draw_contours(frame_painted)

        camera.show(frame)
        

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

camera.end()
